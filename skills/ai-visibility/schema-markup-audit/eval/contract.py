"""Shared outcome validator for schema-markup-audit.

Encodes the non-negotiable rules from ../SKILL.md's Output list and Guardrails,
and the per-type property checklists in ../references/checks.md, as
machine-checkable functions, independent of who produced the text being
checked (a hand-authored golden fixture, or a live model response). Both
run_eval.py (deterministic, golden-fixture layer) and model_harness.py
(gated, live-model layer) import this module so the two layers score
outcomes the same way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores audit-report text and decline-response text.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)
JSON_CODE_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n[ \t]*```", re.DOTALL)
ANY_CODE_BLOCK_RE = re.compile(r"```(?:bash|json)?\s*\n.*?\n[ \t]*```", re.DOTALL)
VALIDATOR_URL_RE = re.compile(
    r"validator\.schema\.org|search\.google\.com/test/rich-results", re.IGNORECASE
)

REQUIRED_SECTIONS = [
    "Existing schema types found",
    "Missing or weak schema",
    "Mismatches with visible content",
    "Recommended JSON-LD changes",
    "Verification tools or commands",
]

# Property checklists per page type, from references/checks.md, plus a
# baseline of generic schema.org properties allowed on any type. Any property
# key used in a "Recommended JSON-LD changes" block that is not in the
# relevant type's checklist (or the baseline) is treated as an invented /
# decorative property, per the "prefer schema that clarifies real entities
# over decorative markup" guardrail.
BASELINE_PROPERTIES = {"@context", "@type", "name", "url", "description", "image", "identifier"}

PAGE_TYPE_PROPERTIES = {
    "Product": BASELINE_PROPERTIES | {
        "sku", "gtin", "brand", "offers", "price", "priceCurrency",
        "availability", "hasVariant", "aggregateRating", "review",
    },
    "Organization": BASELINE_PROPERTIES | {
        "logo", "sameAs", "contactPoint", "telephone", "contactType",
    },
    "Article": BASELINE_PROPERTIES | {
        "headline", "datePublished", "dateModified", "author", "publisher",
    },
    "FAQPage": BASELINE_PROPERTIES | {
        "mainEntity", "acceptedAnswer", "text",
    },
    "BreadcrumbList": BASELINE_PROPERTIES | {"itemListElement", "position", "item"},
    "LocalBusiness": BASELINE_PROPERTIES | {
        "address", "geo", "openingHoursSpecification", "telephone",
        "streetAddress", "addressLocality", "addressRegion", "postalCode",
        "addressCountry", "latitude", "longitude", "dayOfWeek", "opens", "closes",
    },
    "SoftwareApplication": BASELINE_PROPERTIES | {
        "applicationCategory", "operatingSystem", "offers", "price",
    },
}


@dataclass
class ContractResult:
    failures: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def add(self, message: str) -> None:
        self.failures.append(message)


def parse_sections(report_text: str) -> dict:
    """Split an audit report into {heading: body} by '## ' headings."""
    matches = list(SECTION_RE.finditer(report_text))
    sections = {}
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(report_text)
        sections[match.group(1).strip()] = report_text[start:end]
    return sections


def _walk_properties(node, found: set) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key not in ("@context", "@type"):
                found.add(key)
            _walk_properties(value, found)
    elif isinstance(node, list):
        for item in node:
            _walk_properties(item, found)


def check_audit_contract(
    report_text: str,
    page_type: str,
    expect_mismatch: bool = False,
    forbidden_properties: list | None = None,
) -> ContractResult:
    """Deterministic, non-negotiable checks from SKILL.md's Output list,
    Guardrails, and references/checks.md's property checklists.

    - all five required Output sections are present
    - "Recommended JSON-LD changes" contains at least one fenced ```json
      block that parses as valid JSON-LD (has an @type)
    - every property used in that JSON-LD is in the page type's checklist
      (or the generic baseline) — catches invented/decorative properties
    - "Verification tools or commands" carries a runnable command or a
      validator/rich-results URL, never neither
    - "Mismatches with visible content" is non-empty when the fixture
      declares a real mismatch exists
    - none of the fixture's declared forbidden (unsupportable) properties
      appear in the recommended JSON-LD — guards "do not add schema claims
      that are not visible or supportable on the page"
    """
    result = ContractResult()
    sections = parse_sections(report_text)

    for heading in REQUIRED_SECTIONS:
        if heading not in sections:
            result.add(f"missing required '## {heading}' section")

    if "Recommended JSON-LD changes" in sections:
        body = sections["Recommended JSON-LD changes"]
        json_blocks = JSON_CODE_BLOCK_RE.findall(body)
        if not json_blocks:
            result.add(
                "'Recommended JSON-LD changes' section has no fenced ```json code block"
            )
        else:
            allowed = PAGE_TYPE_PROPERTIES.get(page_type, BASELINE_PROPERTIES)
            for raw in json_blocks:
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as exc:
                    result.add(f"recommended JSON-LD block is not valid JSON: {exc}")
                    continue

                found_properties = set()
                _walk_properties(parsed, found_properties)
                unknown = found_properties - allowed
                if unknown:
                    result.add(
                        f"recommended JSON-LD uses properties not in the {page_type} "
                        f"checklist (references/checks.md) or baseline: {sorted(unknown)}"
                    )

                forbidden = set(forbidden_properties or [])
                fabricated = found_properties & forbidden
                if fabricated:
                    result.add(
                        f"recommended JSON-LD includes properties not supportable by "
                        f"visible page content: {sorted(fabricated)}"
                    )

    if "Verification tools or commands" in sections:
        body = sections["Verification tools or commands"]
        if not ANY_CODE_BLOCK_RE.search(body) and not VALIDATOR_URL_RE.search(body):
            result.add(
                "'Verification tools or commands' has neither a runnable command nor "
                "a validator/rich-results URL"
            )

    if expect_mismatch and "Mismatches with visible content" in sections:
        body = sections["Mismatches with visible content"].strip()
        if not body or body.lower().startswith("none"):
            result.add(
                "fixture declares a real content mismatch but "
                "'Mismatches with visible content' is empty or says none"
            )

    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a full
    audit report, and must contain at least one of the expected decline/defer
    or guardrail-refusal signals."""
    result = ContractResult()

    sections = parse_sections(response_text)
    present_required = [h for h in REQUIRED_SECTIONS if h in sections]
    if len(present_required) >= 3:
        result.add(
            "response contains most/all audit-report sections — a full schema audit "
            "was fabricated for an input that should have been declined or deferred"
        )

    if decline_signal_patterns:
        matched = any(
            re.search(pattern, response_text, re.IGNORECASE) for pattern in decline_signal_patterns
        )
        if not matched:
            result.add(
                f"response does not match any expected decline signal pattern: "
                f"{decline_signal_patterns}"
            )

    return result

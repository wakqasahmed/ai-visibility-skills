"""Shared outcome validator for sitemap-discovery-audit.

Encodes the non-negotiable rules from ../SKILL.md's Output/Guardrails
sections and ../references/checks.md's "Evidence discipline" note as
machine-checkable functions, independent of who produced the text being
checked (a hand-authored golden fixture, or a live model response). Both
run_eval.py (deterministic, golden-fixture layer) and model_harness.py
(gated, live-model layer) import this module so the two layers score
outcomes the same way and cannot silently drift apart.

This module contains no network calls, no model calls, and no
fixture-specific logic — it only parses/scores sitemap-audit report text
and decline-response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "Sitemap paths found",
    "Coverage gaps",
    "Broken or blocked URLs",
    "Canonical and redirect issues",
    "Priority fixes",
]

SECTION_HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)
URL_RE = re.compile(r"https?://\S+")
STATUS_CODE_RE = re.compile(r"\b[1-5]\d{2}\b")
CODE_SPAN_RE = re.compile(r"`[^`]+`")
INDEXING_DISCLAIMER_RE = re.compile(
    r"sitemap (presence|inclusion)[^.\n]*(is )?not[^.\n]*(proof|guarantee)[^.\n]*index",
    re.IGNORECASE,
)
PRIORITY_LABEL_RE = re.compile(r"\bP[0-3]\b|priority\s*:", re.IGNORECASE)
FACETED_NOISE_RE = re.compile(
    r"facet|generated url|url noise|crawl noise|parameter(ized)? url|query string",
    re.IGNORECASE,
)
NO_FINDINGS_RE = re.compile(
    r"no (significant )?(coverage )?gaps|none found|no broken (or blocked )?urls|"
    r"no issues found|nothing to (flag|fix)",
    re.IGNORECASE,
)


@dataclass
class ContractResult:
    failures: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def add(self, message: str) -> None:
        self.failures.append(message)


def parse_sections(report_text: str) -> dict:
    """Split a report into {heading: body} using '## ' headings."""
    matches = list(SECTION_HEADING_RE.finditer(report_text))
    sections = {}
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(report_text)
        sections[match.group(1).strip()] = report_text[start:end]
    return sections


def _bullets(body: str) -> list:
    return [line.strip()[2:].strip() for line in body.splitlines() if line.strip().startswith("- ")]


def check_report_contract(report_text: str, meta: dict | None = None) -> ContractResult:
    """Deterministic, non-negotiable checks from SKILL.md's Output/Guardrails
    and references/checks.md's evidence-discipline note.

    - all five required sections are present
    - the report explicitly disclaims that sitemap presence is not proof of
      indexing (never silently assumed)
    - every finding bullet under Coverage gaps / Broken or blocked URLs /
      Canonical and redirect issues cites a URL plus either an HTTP status
      code or a command/evidence code span — never a bare claim
    - every Priority fixes bullet carries an explicit priority label, so
      fixes are ranked rather than dumped as an exhaustive URL count
    - if the fixture expects a faceted/generated-URL crawl-noise flag, the
      report must mention it somewhere
    """
    meta = meta or {}
    result = ContractResult()
    sections = parse_sections(report_text)

    for heading in REQUIRED_SECTIONS:
        if heading not in sections:
            result.add(f"missing required '## {heading}' section")

    if not INDEXING_DISCLAIMER_RE.search(report_text):
        result.add(
            "report never explicitly disclaims that sitemap presence/inclusion "
            "is not proof of indexing"
        )

    evidence_sections = ["Coverage gaps", "Broken or blocked URLs", "Canonical and redirect issues"]
    any_finding_bullets = False
    for heading in evidence_sections:
        body = sections.get(heading, "")
        bullets = _bullets(body)
        for bullet in bullets:
            if NO_FINDINGS_RE.search(bullet):
                continue
            any_finding_bullets = True
            has_url = bool(URL_RE.search(bullet))
            has_evidence = bool(STATUS_CODE_RE.search(bullet) or CODE_SPAN_RE.search(bullet))
            if not has_url:
                result.add(f"finding in '{heading}' has no URL cited: {bullet!r}")
            if not has_evidence:
                result.add(
                    f"finding in '{heading}' has no HTTP status code or command/evidence "
                    f"cited: {bullet!r}"
                )

    if meta.get("expected_min_findings", 0) > 0 and not any_finding_bullets:
        result.add(
            "fixture expects at least one finding, but no evidenced finding bullets "
            "were found in any of Coverage gaps / Broken or blocked URLs / "
            "Canonical and redirect issues"
        )

    if meta.get("expected_min_findings") == 0:
        for heading in evidence_sections:
            body = sections.get(heading, "")
            if _bullets(body) and not NO_FINDINGS_RE.search(body):
                result.add(
                    f"fixture expects a clean audit (no findings) but '{heading}' has "
                    f"fabricated finding bullets"
                )

    priority_body = sections.get("Priority fixes", "")
    priority_bullets = _bullets(priority_body)
    if meta.get("expected_min_findings", 0) > 0:
        if not priority_bullets:
            result.add("'Priority fixes' section has no bullets despite findings existing")
        for bullet in priority_bullets:
            if not PRIORITY_LABEL_RE.search(bullet):
                result.add(f"'Priority fixes' bullet has no explicit priority label: {bullet!r}")

    if meta.get("expects_faceted_flag") and not FACETED_NOISE_RE.search(report_text):
        result.add(
            "fixture expects faceted/generated-URL crawl-noise to be flagged, but the "
            "report never mentions it"
        )

    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a full
    sitemap-audit report, and must contain at least one expected decline/defer
    signal."""
    result = ContractResult()

    sections = parse_sections(response_text)
    if all(heading in sections for heading in REQUIRED_SECTIONS):
        result.add(
            "response contains all five required report sections — a full sitemap "
            "audit was fabricated for an input that should have been declined or "
            "redirected"
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

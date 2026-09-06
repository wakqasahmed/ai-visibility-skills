"""Shared outcome validator for international-seo-hreflang-audit.

Encodes the non-negotiable rules from skills/ai-visibility/international-seo-hreflang-audit/SKILL.md's
Output list and Guardrails, and the evidence-discipline conventions in
skills/ai-visibility/international-seo-hreflang-audit/references/checks.md.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "target locale matrix",
    "hreflang conformance and reciprocity",
    "canonical alignment",
    "recommended fixes",
    "verification commands",
]

SECTION_HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)

GUARANTEE_WORD_RE = re.compile(
    r"\bguarantee[sd]?\b|\bwill definitely\b|\bwill certainly\b|"
    r"\b100% (cited|indexed|ranked|guaranteed)\b|"
    r"\balways be (cited|included|indexed)\b|\bpromise[sd]?\b",
    re.IGNORECASE,
)
NEGATION_BEFORE_RE = re.compile(
    r"\b(no|not|cannot|can't|won't|will not|never|doesn't|does not|isn't|"
    r"n't|without any)\b",
    re.IGNORECASE,
)


def _has_affirmative_guarantee(text: str) -> bool:
    for match in GUARANTEE_WORD_RE.finditer(text):
        preceding = text[max(0, match.start() - 40):match.start()]
        if NEGATION_BEFORE_RE.search(preceding):
            continue
        return True
    return False


EVIDENCE_KEYWORD_RE = re.compile(
    r"hreflang|x-default|alternate|canonical|xhtml:link|curl|iso",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

RAW_PASS_RE = re.compile(
    r"initial (server )?response|raw html|raw `?curl|raw pass|server-delivered|server response",
    re.IGNORECASE,
)
HYDRATED_PASS_RE = re.compile(
    r"hydrated dom|rendered dom|--dump-dom|headless chrom|after javascript",
    re.IGNORECASE,
)
NON_JS_CRAWLER_RE = re.compile(
    r"non-js|do(es)? not execute javascript|without executing javascript|"
    r"javascript-executing|js-executing",
    re.IGNORECASE,
)


ATX_SECTION_RE = re.compile(r"^#{2,3}\s+(.+)$", re.MULTILINE)


def extract_section(text: str, heading: str) -> str | None:
    """Return the body text under a '##'/'###' heading whose lowercased title
    contains `heading`, up to the next such heading, or None. Requires at
    least two '#' so a '# ' shell comment inside a fenced code block is never
    mistaken for a section heading."""
    matches = list(ATX_SECTION_RE.finditer(text))
    for i, match in enumerate(matches):
        if heading in match.group(1).strip().lower():
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[start:end]
    return None


@dataclass
class ValidationResult:
    passed: bool
    failures: list[str] = field(default_factory=list)

    def add_failure(self, reason: str) -> None:
        self.passed = False
        self.failures.append(reason)


def validate_report_contract(text: str, hydration_only: bool = False) -> ValidationResult:
    result = ValidationResult(passed=True)

    if not text or not text.strip():
        result.add_failure("report is empty")
        return result

    headings = [h.strip().lower() for h in SECTION_HEADING_RE.findall(text)]
    for required in REQUIRED_SECTIONS:
        if not any(required in h for h in headings):
            result.add_failure(f"missing required section: '{required}'")

    if _has_affirmative_guarantee(text):
        result.add_failure("report makes an outcome guarantee (violates guardrails)")

    if not EVIDENCE_KEYWORD_RE.search(text):
        result.add_failure("report contains no technical hreflang/canonical evidence keywords")

    if not INLINE_CODE_RE.search(text) and "```" not in text:
        result.add_failure("report contains no code snippets or inline command evidence")

    if hydration_only:
        conformance = extract_section(text, "hreflang conformance and reciprocity") or ""
        if not RAW_PASS_RE.search(conformance) or not HYDRATED_PASS_RE.search(conformance):
            result.add_failure(
                "fixture is hydration-only but 'Hreflang Conformance and Reciprocity' does "
                "not show both a raw pass and a hydrated-DOM pass - the divergence must be "
                "evidenced, not asserted"
            )
        if not NON_JS_CRAWLER_RE.search(text):
            result.add_failure(
                "fixture is hydration-only but the report never discloses that the gap is "
                "invisible to crawlers that do not execute JavaScript"
            )
        verification = extract_section(text, "verification commands") or ""
        if not HYDRATED_PASS_RE.search(verification):
            result.add_failure(
                "fixture is hydration-only but 'Verification Commands' has no headless/"
                "--dump-dom re-check command"
            )

    return result


def validate_decline_contract(text: str, expected_topic: str | None = None) -> ValidationResult:
    result = ValidationResult(passed=True)
    if not text or not text.strip():
        result.add_failure("decline response is empty")
        return result

    if _has_affirmative_guarantee(text):
        result.add_failure("decline makes an outcome guarantee")

    lower = text.lower()
    decline_signals = ["out of scope", "not applicable", "does not apply", "single-language", "single-region", "delegate", "refer to", "cannot", "recommend"]
    if not any(sig in lower for sig in decline_signals):
        result.add_failure("response does not clearly state boundary or redirection")

    return result

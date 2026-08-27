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
    r"guarantee[sd]?|will definitely|will certainly|100% (cited|indexed|ranked|guaranteed)|"
    r"always be (cited|included|indexed)|promise[sd]?",
    re.IGNORECASE,
)
NEGATION_BEFORE_RE = re.compile(
    r"\b(no|not|cannot|can't|won't|will not|never|doesn't|does not|isn't|"
    r"n't|without any)\b[^.]{0,40}$",
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


@dataclass
class ValidationResult:
    passed: bool
    failures: list[str] = field(default_factory=list)

    def add_failure(self, reason: str) -> None:
        self.passed = False
        self.failures.append(reason)


def validate_report_contract(text: str) -> ValidationResult:
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

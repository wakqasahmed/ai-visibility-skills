"""Shared outcome validator for ai-share-of-voice-audit."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "multi-model brand mention & citation matrix",
    "share of voice calculation & benchmark",
    "competitor displacement & source attribution",
    "prioritized remediation & displacement playbook",
    "verification methodology",
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
SENTENCE_HEAD_RE = re.compile(r"(?:^|[.!?\n])([^.!?\n]*)$")


def _has_affirmative_guarantee(text: str) -> bool:
    for match in GUARANTEE_WORD_RE.finditer(text):
        head = SENTENCE_HEAD_RE.search(text[: match.start()])
        preceding = head.group(1) if head else ""
        if NEGATION_BEFORE_RE.search(preceding):
            continue
        return True
    return False


# Deliberately orthogonal to REQUIRED_SECTIONS and to CAPTURE_DATE_RE: these terms
# appear only in actual transcript evidence, so this check can fail independently of
# the heading and capture-date checks.
EVIDENCE_KEYWORD_RE = re.compile(
    r"\bmentioned\b|\bunmentioned\b|\bexcluded\b|cited url|\btranscript\b|"
    r"\bcurl\b|\bschema\b",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

# "12 / 34 = 35.3%" - every reported percentage must be recomputable from the
# counts printed beside it (SKILL.md step 3).
SOV_RATIO_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s*=\s*([\d.]+)\s*%")
PROVENANCE_RE = re.compile(r"\[(Measured|Derived)\]")
CAPTURE_DATE_RE = re.compile(r"capture date[^\n]*\d{4}-\d{2}-\d{2}", re.IGNORECASE)
FRONTMATTER_DESCRIPTION_RE = re.compile(
    r"^---\s*$.*?^description:\s*(.+?)\s*$.*?^---\s*$",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
TRANSCRIPT_TRIGGER_RE = re.compile(
    r"\b(use|analy[sz]e)\b.*\boperator-supplied\b.*\banswer transcripts?\b",
    re.IGNORECASE,
)
LIVE_COLLECTION_EXCLUSION_RE = re.compile(
    r"\b(does not|do not|not for|never)\b.*\b(collect|query)\w*\b.*\blive answers?\b",
    re.IGNORECASE,
)

RATIO_TOLERANCE_PCT = 0.1


@dataclass
class ValidationResult:
    passed: bool
    failures: list[str] = field(default_factory=list)

    def add_failure(self, reason: str) -> None:
        self.passed = False
        self.failures.append(reason)


def validate_trigger_contract(skill_text: str) -> ValidationResult:
    result = ValidationResult(passed=True)
    match = FRONTMATTER_DESCRIPTION_RE.search(skill_text)
    if not match:
        result.add_failure("skill frontmatter has no description")
        return result

    description = match.group(1)
    if not TRANSCRIPT_TRIGGER_RE.search(description):
        result.add_failure(
            "description does not say to use the skill to analyze operator-supplied "
            "answer transcripts"
        )
    if not LIVE_COLLECTION_EXCLUSION_RE.search(description):
        result.add_failure(
            "description does not say the skill is not for collecting or querying live answers"
        )

    return result


def _check_numeric_coherence(text: str, result: ValidationResult) -> None:
    matches = SOV_RATIO_RE.findall(text)
    if not matches:
        result.add_failure(
            "no share of voice figure printed as 'brand / total = pct%' "
            "(percentages must be recomputable from printed counts)"
        )
        return

    for numerator, denominator, stated in matches:
        num, den, pct = int(numerator), int(denominator), float(stated)
        if den == 0:
            result.add_failure(f"share of voice figure '{num} / {den}' divides by zero")
            continue
        if num > den:
            result.add_failure(
                f"share of voice figure '{num} / {den}' exceeds its own denominator"
            )
            continue
        expected = num / den * 100.0
        if abs(expected - pct) > RATIO_TOLERANCE_PCT:
            result.add_failure(
                f"share of voice figure '{num} / {den} = {stated}%' does not reconcile "
                f"(recomputes to {expected:.1f}%)"
            )


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
        result.add_failure("report contains no technical share of voice evidence keywords")

    if not INLINE_CODE_RE.search(text) and "```" not in text:
        result.add_failure("report contains no code snippets or inline command evidence")

    if not PROVENANCE_RE.search(text):
        result.add_failure("report labels no figure [Measured] or [Derived]")

    if not CAPTURE_DATE_RE.search(text):
        result.add_failure("report states no capture date for the prompt corpus")

    _check_numeric_coherence(text, result)

    return result


def validate_decline_contract(text: str, expected_topic: str | None = None) -> ValidationResult:
    result = ValidationResult(passed=True)
    if not text or not text.strip():
        result.add_failure("decline response is empty")
        return result

    if _has_affirmative_guarantee(text):
        result.add_failure("decline makes an outcome guarantee")

    lower = text.lower()
    decline_signals = ["out of scope", "not applicable", "does not apply", "delegate", "refer to", "cannot"]
    if not any(sig in lower for sig in decline_signals):
        result.add_failure("response does not clearly state boundary or redirection")

    if expected_topic and expected_topic.lower() not in lower:
        result.add_failure(
            f"decline does not name the expected redirect target: '{expected_topic}'"
        )

    return result

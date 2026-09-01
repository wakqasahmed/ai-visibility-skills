"""Shared outcome validator for semantic-entity-topical-map-audit."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "entity disambiguation & knowledge graph grounding",
    "schema graph reconciliation",
    "topical map & cluster structure",
    "recommended fixes & schema graph",
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
    r"sameas|wikidata|crunchbase|@id|jobtitle|json-ld|ld\+json",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

CLASSIFICATIONS = ("AMBIGUOUS", "PARTIALLY_GROUNDED", "FULLY_RECONCILED")
CLASSIFICATION_LINE_RE = re.compile(
    r"^\s*[-*]?\s*Entity clarity classification:\s*\**\s*([A-Z_]+)\s*\**\s*$",
    re.MULTILINE,
)


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
        result.add_failure("report contains no technical semantic entity evidence keywords")

    if not INLINE_CODE_RE.search(text) and "```" not in text:
        result.add_failure("report contains no code snippets or inline command evidence")

    found = CLASSIFICATION_LINE_RE.findall(text)
    if not found:
        result.add_failure(
            "report has no 'Entity clarity classification: **VALUE**' line"
        )
    elif len(found) > 1:
        result.add_failure(f"report emits {len(found)} classification lines, expected exactly 1")
    elif found[0] not in CLASSIFICATIONS:
        result.add_failure(
            f"classification '{found[0]}' is not one of {'/'.join(CLASSIFICATIONS)}"
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
    decline_signals = [
        "out of scope",
        "not applicable",
        "does not apply",
        "delegate",
        "refer to",
        "cannot",
    ]
    if not any(sig in lower for sig in decline_signals):
        result.add_failure("response does not clearly state boundary or redirection")

    # A response that emits the audit report's own section structure has not declined,
    # whatever boundary language it also contains.
    headings = [h.strip().lower() for h in SECTION_HEADING_RE.findall(text)]
    emitted = [s for s in REQUIRED_SECTIONS if any(s in h for h in headings)]
    if emitted:
        result.add_failure(
            f"decline still emits audit report sections: {emitted}"
        )

    return result

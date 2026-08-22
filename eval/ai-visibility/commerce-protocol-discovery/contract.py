"""Shared outcome validator for commerce-protocol-discovery.

Encodes the non-negotiable rules from
skills/ai-visibility/commerce-protocol-discovery/SKILL.md's Output list and Guardrails, and the
evidence-discipline conventions in
skills/ai-visibility/commerce-protocol-discovery/references/checks.md, as machine-checkable
functions, independent of who produced the text being checked (a hand-authored golden fixture,
or a live model response). Both run_eval.py (deterministic, golden-fixture layer) and
model_harness.py (gated, live-model layer) import this module so the two layers score outcomes
the same way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific logic — it only
parses/scores discovery-report text and decline-response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "site-type classification",
    "ucp business profile",
    "a2a agent card",
    "mcp",
    "catalog feeds",
]

SECTION_HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)

GUARANTEE_WORD_RE = re.compile(
    r"guarantee[sd]?|will definitely|will certainly|100% (cited|indexed|ranked|guaranteed)|"
    r"always be (cited|included|indexed|ranked)|promise[sd]?",
    re.IGNORECASE,
)
NEGATION_BEFORE_RE = re.compile(
    r"\b(no|not|cannot|can't|won't|will not|never|doesn't|does not|isn't|"
    r"n't|without any)\b[^.]{0,40}$",
    re.IGNORECASE,
)


def _has_affirmative_guarantee(text: str) -> bool:
    """True if the text makes an unqualified guarantee/promise claim - i.e. a
    GUARANTEE_WORD_RE match with no negation word in the ~40 chars before it."""
    for match in GUARANTEE_WORD_RE.finditer(text):
        preceding = text[max(0, match.start() - 40):match.start()]
        if NEGATION_BEFORE_RE.search(preceding):
            continue
        return True
    return False


CLOSING_SCOPE_NOTE_RE = re.compile(
    r"full commerce-protocol readiness scoring and remediation is a separate audit capability"
    r".{0,200}only reports what'?s discoverable, not whether it'?s implemented correctly or safely",
    re.IGNORECASE | re.DOTALL,
)

# The 5-state readiness rubric owned by the private commerce-protocol-readiness skill. Any of
# these words used as a scoring verdict (not merely appearing incidentally in prose, e.g. "the
# endpoint is missing" is fine as plain English, but "Status: ready" or "Score: partial" is not)
# is a scope-boundary leak. We flag the rubric-style label pattern rather than the bare word so
# a normal English sentence isn't false-flagged.
SCORING_LABEL_RE = re.compile(
    r"(status|score|rating|verdict|assessment)\s*[:\-]\s*(ready|partial|missing|verified)\b|"
    r"\b(ready|partial|missing|verified)\s*/\s*(ready|partial|missing|verified)\b",
    re.IGNORECASE,
)

REMEDIATION_VERB_RE = re.compile(
    r"\b(recommend(ed|ation)?s?|should implement|next step|remediat\w*|to fix this|to improve "
    r"this|you (should|need to) (add|implement|publish|configure))\b",
    re.IGNORECASE,
)

TRUST_LIFECYCLE_KEYWORD_RE = re.compile(
    r"\b(trust gate|checkout lifecycle|order lifecycle|payment authorization|agent identity "
    r"verification|delegated authority|refund boundary|cancellation boundary)\b",
    re.IGNORECASE,
)

EVIDENCE_STATUS_CODE_RE = re.compile(r"\b[1-5]\d{2}\b")
EVIDENCE_KEYWORD_RE = re.compile(
    r"www-authenticate|401|curl|\.well-known|products\.json|catalog\.json|robots\.txt|"
    r"sitemap|http_code",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

SENSITIVE_PATH_RE = re.compile(
    r"/(admin|wp-admin|wp-login|account|internal|private|dashboard|login|staging)\b",
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


def extract_section(text: str, heading: str) -> str | None:
    """Return the body text under a '## <heading>'-style section (any level 1-3),
    up to the next same-or-higher-level heading, or None if not found."""
    matches = list(SECTION_HEADING_RE.finditer(text))
    for i, match in enumerate(matches):
        if match.group(1).strip().lower().lstrip("#").strip() == heading:
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[start:end]
    return None


def _join_wrapped_bullets(section_text: str) -> list[str]:
    """Collapse a markdown bullet list into one string per bullet, folding in
    soft-wrapped continuation lines (no blank line, no new '- '/'* ' marker)."""
    bullets: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            bullets.append(stripped)
        elif stripped and bullets:
            bullets[-1] += " " + stripped
    return bullets


def check_discovery_contract(
    text: str,
    evidenced_sections: list[str] | None = None,
    forbidden_patterns: list[str] | None = None,
) -> ContractResult:
    """Deterministic, non-negotiable checks for a commerce-protocol-discovery report.

    - all five required sections from SKILL.md's Output list are present
    - the exact closing scope note is present, near-verbatim
    - no 5-state ready/partial/missing/verified scoring label anywhere
    - no remediation recommendation beyond the closing scope note
    - no trust-gate / checkout-lifecycle analysis language
    - every finding bullet in the given evidenced_sections carries inline evidence
    - no outcome-guarantee language anywhere (shared guardrails.md)
    - no recommendation to expose a private/sensitive path
    - none of the fixture's declared forbidden_patterns appear in the response
    """
    result = ContractResult()

    for heading in REQUIRED_SECTIONS:
        if extract_section(text, heading) is None:
            result.add(f"missing required section heading: '{heading}'")

    if not CLOSING_SCOPE_NOTE_RE.search(text):
        result.add(
            "response is missing the required closing scope note about full readiness "
            "scoring/remediation being a separate audit capability"
        )

    if SCORING_LABEL_RE.search(text):
        result.add(
            "response uses a ready/partial/missing/verified scoring label - reproduces the "
            "private commerce-protocol-readiness skill's 5-state rubric, which this skill must "
            "never do"
        )

    if TRUST_LIFECYCLE_KEYWORD_RE.search(text):
        result.add(
            "response analyzes trust gates or checkout/order lifecycle - out of scope for a "
            "discovery-only skill"
        )

    # Remediation verbs are allowed only inside the mandated closing scope sentence itself;
    # any occurrence outside that sentence is an out-of-scope recommendation.
    text_without_closing_note = CLOSING_SCOPE_NOTE_RE.sub("", text)
    if REMEDIATION_VERB_RE.search(text_without_closing_note):
        result.add(
            "response makes a remediation recommendation beyond the single mandated closing "
            "scope sentence - out of scope for a discovery-only skill"
        )

    for section_name in evidenced_sections or []:
        section_text = extract_section(text, section_name)
        if section_text is None:
            continue
        bullets = _join_wrapped_bullets(section_text)
        for bullet in bullets:
            has_inline_code = bool(INLINE_CODE_RE.search(bullet))
            has_evidence = bool(
                EVIDENCE_STATUS_CODE_RE.search(bullet) or EVIDENCE_KEYWORD_RE.search(bullet)
            )
            if not (has_inline_code and has_evidence):
                result.add(
                    f"finding bullet in '{section_name}' lacks cited evidence "
                    f"(status code, endpoint, or probe keyword) in inline code: "
                    f"{bullet.strip()!r}"
                )

    if _has_affirmative_guarantee(text):
        result.add(
            "response claims or implies a guaranteed AI platform outcome - "
            "violates shared guardrails.md 'No outcome guarantees'"
        )

    if SENSITIVE_PATH_RE.search(text):
        result.add(
            "response references a private/sensitive path - violates shared guardrails.md"
        )

    for pattern in forbidden_patterns or []:
        if re.search(pattern, text, re.IGNORECASE):
            result.add(
                f"response contains a forbidden fabricated pattern: {pattern!r} - "
                f"violates the 'do not invent unverifiable content' guardrail"
            )

    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a full discovery
    report, must not leak scoring language, and must contain at least one of the expected
    decline/defer/redirect signals."""
    result = ContractResult()

    present_sections = [h for h in REQUIRED_SECTIONS if extract_section(response_text, h) is not None]
    if len(present_sections) >= 3:
        result.add(
            f"response fabricates a full commerce-protocol-discovery report ({len(present_sections)}/"
            f"{len(REQUIRED_SECTIONS)} required sections present) for an input that "
            f"should have been declined, redirected, or deferred"
        )

    if _has_affirmative_guarantee(response_text):
        result.add(
            "response claims or implies a guaranteed AI platform outcome - "
            "violates shared guardrails.md 'No outcome guarantees'"
        )

    if SCORING_LABEL_RE.search(response_text):
        result.add(
            "response uses a ready/partial/missing/verified scoring label - reproduces the "
            "private commerce-protocol-readiness skill's 5-state rubric"
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

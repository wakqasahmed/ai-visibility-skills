"""Shared outcome validator for ecommerce-technical-seo-audit.

Encodes the non-negotiable rules from
skills/ai-visibility/ecommerce-technical-seo-audit/SKILL.md's Output list and Guardrails, and
the evidence-discipline conventions in
skills/ai-visibility/ecommerce-technical-seo-audit/references/checks.md, as machine-checkable
functions, independent of who produced the text being checked (a hand-authored golden fixture,
or a live model response). Both run_eval.py (deterministic, golden-fixture layer) and
model_harness.py (gated, live-model layer) import this module so the two layers score outcomes
the same way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific logic — it only
parses/scores audit-report text and decline-response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "sample scope",
    "thin category/collection page findings",
    "faceted-navigation duplicate url findings",
    "orphan page findings",
    "discontinued-product handling findings",
    "recommended fixes",
    "verification commands",
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


EVIDENCE_STATUS_CODE_RE = re.compile(r"\b[1-5]\d{2}\b")
EVIDENCE_KEYWORD_RE = re.compile(
    r"canonical|noindex|robots\.txt|sitemap|word count|redirect|soft 404|410|curl|href",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

SENSITIVE_PATH_RE = re.compile(
    r"/(admin|wp-admin|wp-login|account|checkout|cart|internal|private|dashboard|login|staging)\b",
    re.IGNORECASE,
)

RECOMMENDED_FIXES_ACTIONABLE_RE = re.compile(r"`[^`]+`|```", re.MULTILINE)
HOMEPAGE_REDIRECT_TARGET_RE = re.compile(
    r"->\s*https?://[^/\s]+/?\s*$|Location:\s*https?://[^/\s]+/?\s*$",
    re.MULTILINE,
)

FULL_CATALOG_CLAIM_RE = re.compile(
    r"\b(all|entire|every|whole) (product|category|categories|catalog|catalogue|page)s?\b"
    r"(?![^.]{0,60}\bwas not\b)(?![^.]{0,60}\bnot checked\b)",
    re.IGNORECASE,
)
SAMPLE_DISCLOSURE_RE = re.compile(
    r"\bsample\b|\bsampled\b|\b3-5\b|\b3 to 5\b|not a full[- ]catalog|not the (entire|full) catalog",
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


def check_audit_contract(
    text: str,
    evidenced_sections: list[str] | None = None,
    forbidden_patterns: list[str] | None = None,
) -> ContractResult:
    """Deterministic, non-negotiable checks for an ecommerce-technical-seo-audit report.

    - all seven required sections from SKILL.md's Output list are present
    - "Sample scope" discloses this is a sample, not a full-catalog crawl
    - no claim that the full catalog / all products / all categories was checked
    - "Recommended fixes" contains concrete, actionable content
    - "Verification commands" contains a re-runnable curl command
    - every finding bullet in the given evidenced_sections carries inline evidence
    - no outcome-guarantee language anywhere (shared guardrails.md)
    - no recommendation to expose a private/sensitive path
    - no recommendation to redirect a discontinued product to the homepage/unrelated page
    - none of the fixture's declared forbidden_patterns appear in the response
    """
    result = ContractResult()

    for heading in REQUIRED_SECTIONS:
        if extract_section(text, heading) is None:
            result.add(f"missing required section heading: '{heading}'")

    scope = extract_section(text, "sample scope")
    if scope is not None and not SAMPLE_DISCLOSURE_RE.search(scope):
        result.add(
            "'Sample scope' section does not disclose this is a sample / not a full-catalog "
            "crawl - required by SKILL.md's scope note"
        )

    if FULL_CATALOG_CLAIM_RE.search(text):
        result.add(
            "response claims or implies the full catalog / all products / all categories were "
            "checked - violates the spot-check scope boundary in SKILL.md"
        )

    recommended = extract_section(text, "recommended fixes")
    if recommended is not None:
        if not RECOMMENDED_FIXES_ACTIONABLE_RE.search(recommended):
            result.add(
                "'Recommended fixes' section has no concrete inline code or fenced "
                "block - recommendation is not actionable/verifiable"
            )
        if HOMEPAGE_REDIRECT_TARGET_RE.search(recommended):
            result.add(
                "'Recommended fixes' code block redirects to a bare domain root (homepage) - "
                "violates the checks.md guidance against irrelevant-target redirects"
            )

    verification = extract_section(text, "verification commands")
    if verification is not None:
        if "curl" not in verification.lower():
            result.add(
                "'Verification commands' section has no curl (or equivalent "
                "re-runnable) command"
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
                    f"(status code or concrete markup/attribute) in inline code: "
                    f"{bullet.strip()!r}"
                )

    if _has_affirmative_guarantee(text):
        result.add(
            "response claims or implies a guaranteed AI platform outcome - "
            "violates shared guardrails.md 'No outcome guarantees'"
        )

    if SENSITIVE_PATH_RE.search(recommended or ""):
        result.add(
            "'Recommended fixes' references exposing a private/sensitive path - "
            "violates shared guardrails.md"
        )

    for pattern in forbidden_patterns or []:
        if re.search(pattern, text, re.IGNORECASE):
            result.add(
                f"response contains a forbidden fabricated pattern: {pattern!r} - "
                f"violates the 'do not invent unverifiable content' guardrail"
            )

    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a full
    audit report, and must contain at least one of the expected decline/defer/
    redirect signals."""
    result = ContractResult()

    present_sections = [h for h in REQUIRED_SECTIONS if extract_section(response_text, h) is not None]
    if len(present_sections) >= 4:
        result.add(
            f"response fabricates a full ecommerce-technical-seo-audit report ({len(present_sections)}/"
            f"{len(REQUIRED_SECTIONS)} required sections present) for an input that "
            f"should have been declined, redirected, or deferred"
        )

    if _has_affirmative_guarantee(response_text):
        result.add(
            "response claims or implies a guaranteed AI platform outcome - "
            "violates shared guardrails.md 'No outcome guarantees'"
        )

    if FULL_CATALOG_CLAIM_RE.search(response_text):
        result.add(
            "response claims or implies the full catalog was checked - violates the spot-check "
            "scope boundary in SKILL.md"
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

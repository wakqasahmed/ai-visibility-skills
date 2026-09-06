"""Shared outcome validator for image-audit.

Encodes the non-negotiable rules from skills/ai-visibility/image-audit/SKILL.md's
Output list and Guardrails, and the evidence-discipline conventions in
skills/ai-visibility/image-audit/references/checks.md, as machine-checkable
functions, independent of who produced the text being checked (a hand-authored
golden fixture, or a live model response). Both run_eval.py (deterministic,
golden-fixture layer) and model_harness.py (gated, live-model layer) import
this module so the two layers score outcomes the same way and cannot silently
drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores audit-report text and decline-response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "alt text coverage and quality summary",
    "image sitemap coverage summary",
    "imageobject schema presence and completeness",
    "fetchability findings",
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
    r"alt=|\balt\b|image:loc|image:image|noscript|data-src|data-lazy|imageobject|curl",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

SENSITIVE_PATH_RE = re.compile(
    r"/(admin|wp-admin|wp-login|account|checkout|cart|internal|private|dashboard|login|staging)\b",
    re.IGNORECASE,
)

RECOMMENDED_FIXES_ACTIONABLE_RE = re.compile(r"`[^`]+`|```", re.MULTILINE)

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
    hydration_only: bool = False,
) -> ContractResult:
    """Deterministic, non-negotiable checks for an image-audit report.

    - all six required sections from SKILL.md's Output list are present
    - "Recommended fixes" contains concrete, actionable content (inline code
      or a fenced block), not vague prose only
    - "Verification commands" contains a re-runnable curl command
    - every finding bullet in the given evidenced_sections carries inline
      evidence (a status code or a concrete markup/attribute keyword) -
      evidence discipline from references/checks.md
    - no outcome-guarantee language anywhere (shared guardrails.md)
    - no recommendation to expose a private/sensitive path
    - none of the fixture's declared forbidden patterns (e.g. an invented,
      unverifiable alt-text string) appear in the response - per the
      "do not write alt text describing something not depicted" guardrail
    - hydration_only fixtures (an image tag only exists after client-side
      hydration): "Fetchability findings" must show both the raw pass and
      the hydrated pass and disclose that the gap is invisible to
      non-JS-executing crawlers, and "Verification commands" must include a
      headless/--dump-dom re-check, not curl alone
    """
    result = ContractResult()

    for heading in REQUIRED_SECTIONS:
        if extract_section(text, heading) is None:
            result.add(f"missing required section heading: '{heading}'")

    recommended = extract_section(text, "recommended fixes")
    if recommended is not None:
        if not RECOMMENDED_FIXES_ACTIONABLE_RE.search(recommended):
            result.add(
                "'Recommended fixes' section has no concrete inline code or fenced "
                "block - recommendation is not actionable/verifiable"
            )

    verification = extract_section(text, "verification commands")
    if verification is not None:
        if "curl" not in verification.lower():
            result.add(
                "'Verification commands' section has no curl (or equivalent "
                "re-runnable) command"
            )
        if hydration_only and not HYDRATED_PASS_RE.search(verification):
            result.add(
                "fixture is hydration-only but 'Verification commands' has no headless/"
                "--dump-dom re-check command"
            )

    if hydration_only:
        fetchability = extract_section(text, "fetchability findings") or ""
        if not RAW_PASS_RE.search(fetchability) or not HYDRATED_PASS_RE.search(fetchability):
            result.add(
                "fixture is hydration-only but 'Fetchability findings' does not show both "
                "a raw pass and a hydrated-DOM pass - the divergence must be evidenced, not "
                "asserted"
            )
        if not NON_JS_CRAWLER_RE.search(fetchability):
            result.add(
                "fixture is hydration-only but 'Fetchability findings' never discloses that "
                "the gap is invisible to crawlers that do not execute JavaScript"
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
    if len(present_sections) >= 3:
        result.add(
            f"response fabricates a full image-audit report ({len(present_sections)}/"
            f"{len(REQUIRED_SECTIONS)} required sections present) for an input that "
            f"should have been declined, redirected, or deferred"
        )

    if _has_affirmative_guarantee(response_text):
        result.add(
            "response claims or implies a guaranteed AI platform outcome - "
            "violates shared guardrails.md 'No outcome guarantees'"
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

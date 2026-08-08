"""Shared outcome validator for robots-ai-crawler-audit.

Encodes the non-negotiable rules from ../SKILL.md's Output/Guardrails sections,
../references/checks.md's evidence-discipline note, and the shared
../../references/guardrails.md rules, as machine-checkable functions -
independent of who produced the text being checked (a hand-authored golden
fixture, or a live model response). Both run_eval.py (deterministic,
golden-fixture layer) and model_harness.py (gated, live-model layer) import
this module so the two layers score outcomes the same way and cannot
silently drift apart.

This module contains no network calls, no model calls, and no
fixture-specific logic - it only parses/scores audit-report text and
decline-response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_SECTIONS = [
    "current crawler policy summary",
    "blocked high-value paths",
    "ai crawler implications",
    "recommended robots.txt changes",
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
    GUARANTEE_WORD_RE match with no negation word in the ~40 chars before it.
    Correctly-behaving text that *disclaims* a guarantee ("does not guarantee
    citation", "no outcome guarantee can be made") must NOT be flagged - only
    text that actually asserts one."""
    for match in GUARANTEE_WORD_RE.finditer(text):
        preceding = text[max(0, match.start() - 40):match.start()]
        if NEGATION_BEFORE_RE.search(preceding):
            continue
        return True
    return False

EVIDENCE_STATUS_CODE_RE = re.compile(r"\b[1-5]\d{2}\b")
EVIDENCE_KEYWORD_RE = re.compile(
    r"disallow|noindex|x-robots-tag|curl|nofollow", re.IGNORECASE
)
INLINE_CODE_RE = re.compile(r"`[^`]+`")

SENSITIVE_PATH_RE = re.compile(
    r"/(admin|wp-admin|wp-login|account|checkout|cart|internal|private|dashboard|login|staging)\b",
    re.IGNORECASE,
)
ALLOW_DIRECTIVE_RE = re.compile(r"^\s*allow\s*:\s*(\S+)", re.IGNORECASE | re.MULTILINE)

BOT_DIRECTIVE_RE = re.compile(r"^\s*user-agent\s*:", re.IGNORECASE | re.MULTILINE)
DISALLOW_OR_ALLOW_RE = re.compile(r"^\s*(disallow|allow)\s*:", re.IGNORECASE | re.MULTILINE)


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


def check_audit_contract(text: str) -> ContractResult:
    """Deterministic, non-negotiable checks for a robots-ai-crawler-audit report.

    - all five required sections from SKILL.md's Output list are present
    - "Recommended robots.txt changes" contains real directive syntax
      (User-agent + Allow/Disallow), not vague prose only
    - "Verification commands" contains a re-runnable curl command
    - every finding bullet under "Blocked high-value paths" carries inline
      evidence (a status code, a robots.txt directive, or a header name) -
      evidence discipline from references/checks.md
    - no outcome-guarantee language anywhere (shared guardrails.md)
    - no recommendation to Allow crawlers into private/sensitive paths
      (shared guardrails.md)
    """
    result = ContractResult()

    for heading in REQUIRED_SECTIONS:
        if extract_section(text, heading) is None:
            result.add(f"missing required section heading: '{heading}'")

    recommended = extract_section(text, "recommended robots.txt changes")
    if recommended is not None:
        if not BOT_DIRECTIVE_RE.search(recommended) or not DISALLOW_OR_ALLOW_RE.search(recommended):
            result.add(
                "'Recommended robots.txt changes' section has no concrete "
                "User-agent + Allow/Disallow directive - recommendation is not "
                "actionable/verifiable"
            )

    verification = extract_section(text, "verification commands")
    if verification is not None:
        if "curl" not in verification.lower():
            result.add(
                "'Verification commands' section has no curl (or equivalent "
                "re-runnable) command"
            )

    blocked_section = extract_section(text, "blocked high-value paths")
    if blocked_section is not None:
        bullets = _join_wrapped_bullets(blocked_section)
        for bullet in bullets:
            has_inline_code = bool(INLINE_CODE_RE.search(bullet))
            has_evidence = bool(
                EVIDENCE_STATUS_CODE_RE.search(bullet) or EVIDENCE_KEYWORD_RE.search(bullet)
            )
            if not (has_inline_code and has_evidence):
                result.add(
                    f"finding bullet lacks cited evidence (status code, robots.txt "
                    f"directive, or header) in inline code: {bullet.strip()!r}"
                )

    if _has_affirmative_guarantee(text):
        result.add(
            "response claims or implies a guaranteed AI platform outcome - "
            "violates shared guardrails.md 'No outcome guarantees'"
        )

    for section_name in ("recommended robots.txt changes",):
        section_text = extract_section(text, section_name)
        if section_text is None:
            continue
        for match in ALLOW_DIRECTIVE_RE.finditer(section_text):
            path = match.group(1)
            if SENSITIVE_PATH_RE.search(path):
                result.add(
                    f"recommends 'Allow: {path}' - exposes a private/sensitive path "
                    f"to crawlers, violates shared guardrails.md"
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
            f"response fabricates a full crawler-audit report ({len(present_sections)}/"
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

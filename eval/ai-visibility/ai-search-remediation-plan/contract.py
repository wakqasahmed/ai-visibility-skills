"""Shared outcome validator for ai-search-remediation-plan.

Encodes the non-negotiable rules from ../references/checks.md and ../SKILL.md's
Guardrails as machine-checkable functions, independent of who produced the text
being checked (a hand-authored golden fixture, or a live model response). Both
run_eval.py (deterministic, golden-fixture layer) and model_harness.py (gated,
live-model layer) import this module so the two layers score outcomes the same
way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores remediation-plan text and decline-response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

TICKET_HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)
CODE_BLOCK_RE = re.compile(r"```(?:bash)?\n.*?\n[ \t]*```", re.DOTALL)
BLOCKER_NOTE_RE = re.compile(r"blocked on", re.IGNORECASE)
BLOCKER_KEYWORD_RE = re.compile(
    r"credential|access|legal|policy owner|cms access|approval", re.IGNORECASE
)

DOMAIN_KEYWORDS = {
    "crawler": re.compile(r"crawler|robots\.txt|user-agent|disallow|gptbot|claudebot|perplexitybot", re.IGNORECASE),
    "sitemap": re.compile(r"sitemap", re.IGNORECASE),
    "schema": re.compile(r"json-ld|schema\.org|structured data", re.IGNORECASE),
    "llms_txt": re.compile(r"llms\.txt", re.IGNORECASE),
    "content": re.compile(r"faq|content gap|thin content|answer(s)? (are|is) (thin|missing)", re.IGNORECASE),
    "citation": re.compile(r"citation|substantiat|savings claim|trust signal", re.IGNORECASE),
}


@dataclass
class Ticket:
    title: str
    body: str

    @property
    def has_verification_command(self) -> bool:
        return bool(CODE_BLOCK_RE.search(self.body))

    @property
    def has_blocker_note(self) -> bool:
        return bool(BLOCKER_NOTE_RE.search(self.body))

    @property
    def mentions_blocker_keyword(self) -> bool:
        return bool(BLOCKER_KEYWORD_RE.search(self.body))

    @property
    def domains_touched(self) -> set:
        return {name for name, pattern in DOMAIN_KEYWORDS.items() if pattern.search(self.body)}


@dataclass
class ContractResult:
    failures: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def add(self, message: str) -> None:
        self.failures.append(message)


def parse_tickets(plan_text: str) -> list:
    """Split a remediation-plan document into one Ticket per '## ' heading."""
    matches = list(TICKET_HEADING_RE.finditer(plan_text))
    tickets = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(plan_text)
        tickets.append(Ticket(title=match.group(1).strip(), body=plan_text[start:end]))
    return tickets


def check_plan_contract(plan_text: str, expected_ticket_count: int | None = None) -> ContractResult:
    """Deterministic, non-negotiable checks from references/checks.md.

    - one heading per ticket (independently identifiable and countable)
    - every ticket has either a re-runnable verification command or an explicit
      "blocked on" note, never neither
    - a ticket mentioning blocker language (credential/access/legal/policy
      owner/cms access/approval) must carry a "blocked on" note, not just a
      verification command — the blocker must not be silently dropped
    - no ticket bundles more than one fix domain (crawler + schema + content, etc.)
    """
    result = ContractResult()
    tickets = parse_tickets(plan_text)

    if not tickets:
        result.add("no '## ' ticket headings found in plan")
        return result

    if expected_ticket_count is not None and len(tickets) != expected_ticket_count:
        result.add(
            f"expected {expected_ticket_count} ticket(s), found {len(tickets)}: "
            f"{[t.title for t in tickets]}"
        )

    for ticket in tickets:
        if not ticket.has_verification_command and not ticket.has_blocker_note:
            result.add(
                f"ticket '{ticket.title}' has neither a re-runnable verification "
                f"command nor an explicit 'blocked on' note"
            )

        if ticket.mentions_blocker_keyword and not ticket.has_blocker_note:
            result.add(
                f"ticket '{ticket.title}' mentions blocker language "
                f"(credential/access/legal/policy owner/cms access/approval) but has "
                f"no explicit 'blocked on' note — blocker may have been silently dropped"
            )

        if len(ticket.domains_touched) > 1:
            result.add(
                f"ticket '{ticket.title}' bundles multiple fix domains "
                f"({sorted(ticket.domains_touched)}) into one ticket"
            )

    return result


def check_blocked_tickets_present(plan_text: str, expected_blocked_titles: list) -> ContractResult:
    """Confirm every expected-to-be-blocked ticket is present and marked blocked."""
    result = ContractResult()
    tickets = {t.title: t for t in parse_tickets(plan_text)}
    for title in expected_blocked_titles:
        ticket = tickets.get(title)
        if ticket is None:
            result.add(f"expected blocked ticket '{title}' not found in plan")
        elif not ticket.has_blocker_note:
            result.add(f"expected blocked ticket '{title}' has no 'blocked on' note")
    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a ticket-shaped
    plan, and must contain at least one of the expected decline/defer signals."""
    result = ContractResult()

    if TICKET_HEADING_RE.search(response_text):
        result.add(
            "response contains '## ' ticket headings — a remediation plan was "
            "fabricated for an input that should have been declined or deferred"
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

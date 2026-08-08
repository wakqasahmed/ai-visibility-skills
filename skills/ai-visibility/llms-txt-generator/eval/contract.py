"""Shared outcome validator for llms-txt-generator.

Encodes the non-negotiable rules from ../SKILL.md (Workflow, Output, Guardrails,
scope boundaries) and ../references/checks.md (structure/format convention,
evidence discipline against fabricated links) as machine-checkable functions,
independent of who produced the text being checked (a hand-authored golden
fixture, or a live model response). Both run_eval.py (deterministic,
golden-fixture layer) and model_harness.py (gated, live-model layer) import
this module so the two layers score outcomes the same way and cannot
silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores llms.txt-draft responses and decline/defer
responses.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

CODE_FENCE_RE = re.compile(r"```(?:markdown|md|text)?\n(.*?)\n```", re.DOTALL)
H1_RE = re.compile(r"^# .+$", re.MULTILINE)
H2_RE = re.compile(r"^## .+$", re.MULTILINE)
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")

REQUIRED_OUTPUT_LABELS = {
    "placement path": re.compile(r"placement path", re.IGNORECASE),
    "source urls used": re.compile(r"source url", re.IGNORECASE),
    "missing recommended urls": re.compile(r"missing (recommended )?(url|page)", re.IGNORECASE),
    "verification steps": re.compile(r"verification", re.IGNORECASE),
}

EXISTING_FILE_ACK_RE = re.compile(r"\b(existing|already (has|serves|contains|exists))\b", re.IGNORECASE)


@dataclass
class ContractResult:
    failures: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def add(self, message: str) -> None:
        self.failures.append(message)


def extract_draft_block(response_text: str) -> str | None:
    """Return the fenced code block containing the proposed llms.txt draft.

    The draft is identified as the first fenced block whose content, once
    stripped, starts with a markdown H1 (`# `) — the llms.txt convention's
    required first line.
    """
    for match in CODE_FENCE_RE.finditer(response_text):
        block = match.group(1)
        if block.strip().startswith("# "):
            return block
    return None


def check_draft_structure(response_text: str, expected_min_sections: int = 1) -> ContractResult:
    """Structural checks from references/checks.md / llmstxt.org convention.

    - a fenced llms.txt draft block exists, starting with an H1 title
    - a short summary line follows the title before the first H2 section
    - at least `expected_min_sections` H2 (`## `) sections
    - every link is markdown-formatted with an http(s) URL (no bare/relative links)
    """
    result = ContractResult()
    draft = extract_draft_block(response_text)
    if draft is None:
        result.add("no fenced llms.txt draft block starting with '# ' (H1) found in response")
        return result

    lines = [line for line in draft.splitlines()]
    if not lines or not lines[0].startswith("# "):
        result.add("draft's first line is not an H1 ('# ' title)")

    h2_matches = list(H2_RE.finditer(draft))
    if len(h2_matches) < expected_min_sections:
        result.add(
            f"expected at least {expected_min_sections} '## ' section(s), found {len(h2_matches)}"
        )

    first_h2_start = h2_matches[0].start() if h2_matches else len(draft)
    preamble = draft[: first_h2_start]
    preamble_body = "\n".join(
        line for line in preamble.splitlines()[1:] if line.strip()
    )
    if not preamble_body:
        result.add("draft has no short summary line between the H1 title and the first '## ' section")

    links = LINK_RE.findall(draft)
    if not links:
        result.add("draft contains no markdown links ('[label](https://...)')")

    return result


def check_no_fabricated_urls(response_text: str, allowed_urls: list) -> ContractResult:
    """Evidence discipline: every URL in the draft must come from verified source
    material, never a URL invented for the draft (references/checks.md)."""
    result = ContractResult()
    draft = extract_draft_block(response_text)
    if draft is None:
        return result
    allowed = set(allowed_urls)
    used = {url for _, url in LINK_RE.findall(draft)}
    unverified = used - allowed
    if unverified:
        result.add(
            f"draft includes URL(s) not present in the verified source material: {sorted(unverified)}"
        )
    return result


def check_no_excluded_urls(response_text: str, excluded_urls: list) -> ContractResult:
    """Thin/duplicate/low-signal pages must not appear in the final draft."""
    result = ContractResult()
    draft = extract_draft_block(response_text)
    if draft is None:
        return result
    used = {url for _, url in LINK_RE.findall(draft)}
    leaked = used & set(excluded_urls)
    if leaked:
        result.add(f"draft includes thin/duplicate/low-signal URL(s) that should have been excluded: {sorted(leaked)}")
    return result


def check_output_sections_present(response_text: str) -> ContractResult:
    """SKILL.md's Output contract: every full response must surface these
    alongside the draft itself, not just the file content."""
    result = ContractResult()
    for label, pattern in REQUIRED_OUTPUT_LABELS.items():
        if not pattern.search(response_text):
            result.add(f"response is missing the required '{label}' output section")
    return result


def check_acknowledges_existing_file(response_text: str) -> ContractResult:
    """checks.md: if /llms.txt already returns 200, review it before drafting a
    replacement — never silently overwrite an existing file's intent."""
    result = ContractResult()
    if not EXISTING_FILE_ACK_RE.search(response_text):
        result.add("response does not acknowledge the existing llms.txt file before proposing changes")
    return result


def check_missing_pages_mentioned(response_text: str, expected_keywords: list) -> ContractResult:
    """SKILL.md Output: 'Missing recommended URLs or pages' must name the
    actual gap, not a placeholder like 'None'."""
    result = ContractResult()
    if not expected_keywords:
        return result
    matched = any(re.search(re.escape(k), response_text, re.IGNORECASE) for k in expected_keywords)
    if not matched:
        result.add(f"response does not name any of the expected missing page(s): {expected_keywords}")
    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate an
    llms.txt-shaped draft, and must contain at least one expected
    decline/defer/redirect signal."""
    result = ContractResult()

    draft = extract_draft_block(response_text)
    if draft is not None and H1_RE.search(draft) and H2_RE.search(draft):
        result.add(
            "response contains a fenced H1+H2 llms.txt draft — a file was fabricated "
            "for an input that should have been declined or deferred"
        )

    if decline_signal_patterns:
        matched = any(
            re.search(pattern, response_text, re.IGNORECASE) for pattern in decline_signal_patterns
        )
        if not matched:
            result.add(
                f"response does not match any expected decline signal pattern: {decline_signal_patterns}"
            )

    return result

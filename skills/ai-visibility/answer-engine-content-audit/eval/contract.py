"""Shared outcome validator for answer-engine-content-audit.

Encodes the non-negotiable rules from ../references/checks.md, ../SKILL.md's
Output/Guardrails sections, and ../../references/guardrails.md's "No fabrication"
rule as machine-checkable functions, independent of who produced the text being
checked (a hand-authored golden fixture, or a live model response). Both
run_eval.py (deterministic, golden-fixture layer) and model_harness.py (gated,
live-model layer) import this module so the two layers score outcomes the same
way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores content-audit finding text and decline-response
text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

FINDING_HEADING_RE = re.compile(r"^## Finding: (.+)$", re.MULTILINE)
FIELD_RE = {
    "url": re.compile(r"^- URL:\s*(.+)$", re.MULTILINE),
    "question": re.compile(r"^- Question:\s*(.+)$", re.MULTILINE),
    "command": re.compile(r"^- Command:\s*(.+)$", re.MULTILINE),
    "observed": re.compile(r"^- Observed:\s*(.+)$", re.MULTILINE),
    "status": re.compile(r"^- Status:\s*(\S+)$", re.MULTILINE),
    "severity": re.compile(r"^- Severity:\s*(\S+)$", re.MULTILINE),
}

VALID_STATUSES = {"missing", "vague", "unciteable"}
VALID_SEVERITIES = {"critical", "important", "optional"}

ABSENCE_PATTERN_RE = re.compile(
    r"no match|no output|nothing returned|empty|blank|not found|404|zero results|no text"
    r"|\b0\b|no mention|none\b|no comparison|no .*language|nowhere",
    re.IGNORECASE,
)
CHECK_COMMAND_RE = re.compile(r"curl|grep", re.IGNORECASE)


@dataclass
class Finding:
    title: str
    url: str | None
    question: str | None
    command: str | None
    observed: str | None
    status: str | None
    severity: str | None


@dataclass
class ContractResult:
    failures: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def add(self, message: str) -> None:
        self.failures.append(message)


def _extract_field(name: str, body: str) -> str | None:
    match = FIELD_RE[name].search(body)
    return match.group(1).strip() if match else None


def parse_findings(report_text: str) -> list:
    """Split a content-audit report into one Finding per '## Finding: ' heading."""
    matches = list(FINDING_HEADING_RE.finditer(report_text))
    findings = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(report_text)
        body = report_text[start:end]
        findings.append(
            Finding(
                title=match.group(1).strip(),
                url=_extract_field("url", body),
                question=_extract_field("question", body),
                command=_extract_field("command", body),
                observed=_extract_field("observed", body),
                status=_extract_field("status", body),
                severity=_extract_field("severity", body),
            )
        )
    return findings


def check_report_contract(report_text: str, expected_finding_count: int | None = None) -> ContractResult:
    """Deterministic, non-negotiable checks from references/checks.md + SKILL.md.

    - one heading per finding (independently identifiable and countable)
    - every finding names a URL, the question it was meant to answer, the
      command run, the observed excerpt, a status, and a severity ("Evidence
      discipline" in checks.md)
    - status must be one of missing/vague/unciteable (this report exists to
      surface gaps, not to certify already-good answers)
    - severity must be one of critical/important/optional
    - the command must reflect an actual content-pull check (curl/grep), not
      an assertion with no verification step
    - status=missing/unciteable must not be paired with a fabricated
      substantive excerpt — the observed field must show real absence
      evidence ("no fabrication" guardrail: do not claim a gap without
      pulling the actual rendered text first)
    - status=vague must be paired with a real (non-absence) excerpt proving
      the weak answer actually exists, not just an assertion
    """
    result = ContractResult()
    findings = parse_findings(report_text)

    if not findings:
        result.add("no '## Finding: ' headings found in report")
        return result

    if expected_finding_count is not None and len(findings) != expected_finding_count:
        result.add(
            f"expected {expected_finding_count} finding(s), found {len(findings)}: "
            f"{[f.title for f in findings]}"
        )

    for f in findings:
        for field_name in ("url", "question", "command", "observed", "status", "severity"):
            if not getattr(f, field_name):
                result.add(f"finding '{f.title}' is missing required field '{field_name}'")

        if f.status and f.status.lower() not in VALID_STATUSES:
            result.add(
                f"finding '{f.title}' has status '{f.status}', expected one of {sorted(VALID_STATUSES)}"
            )

        if f.severity and f.severity.lower() not in VALID_SEVERITIES:
            result.add(
                f"finding '{f.title}' has severity '{f.severity}', expected one of {sorted(VALID_SEVERITIES)}"
            )

        if f.command and not CHECK_COMMAND_RE.search(f.command):
            result.add(
                f"finding '{f.title}' has a Command field that does not reflect an actual "
                f"content-pull check (no curl/grep) — the gap must be verified against "
                f"rendered content, not asserted"
            )

        if f.status and f.observed:
            is_absence = bool(ABSENCE_PATTERN_RE.search(f.observed))
            status_lower = f.status.lower()
            if status_lower in {"missing", "unciteable"} and not is_absence:
                result.add(
                    f"finding '{f.title}' has status '{f.status}' but Observed text does not "
                    f"show absence evidence — looks like a fabricated excerpt for a claimed gap"
                )
            if status_lower == "vague" and is_absence:
                result.add(
                    f"finding '{f.title}' has status 'vague' but Observed text shows no actual "
                    f"excerpt was captured — vagueness must be evidenced by real (weak) text, "
                    f"not asserted"
                )

    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a content-gap
    report, and must contain at least one of the expected decline/defer signals."""
    result = ContractResult()

    if FINDING_HEADING_RE.search(response_text):
        result.add(
            "response contains '## Finding: ' headings — a content-gap report was "
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

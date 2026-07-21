"""Shared outcome validator for ai-visibility-audit.

Encodes the non-negotiable rules from ../SKILL.md's "Output"/"Guardrails"
sections as machine-checkable functions, independent of who produced the
report being checked (a hand-authored golden fixture, or a live model
response). Both run_outcome_eval.py (deterministic, golden-fixture layer) and
model_harness.py (gated, live-model layer) import this module so the two
layers score outcomes the same way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores audit-report text and decline-response text.

Note: this is a *separate* validator from the pre-existing
scripts/../run_eval.py + fixture/, which hand-reimplements the commands in
references/checks.md against a single frozen snapshot. That script proves
the checks.md commands are internally consistent; this module proves the
skill's *reporting contract* (severity/evidence/delegation/no-guarantee,
plus should-not-use restraint) holds across a broader scenario set.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

FINDING_RE = re.compile(r"^- \[(CRITICAL|IMPORTANT|OPTIONAL)\] (.+)$", re.MULTILINE)
OVERALL_RE = re.compile(r"^Overall:\s*(ready|partially ready|blocked)\s*$", re.IGNORECASE | re.MULTILINE)
EVIDENCE_LINE_RE = re.compile(r"^\s*evidence:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
DELEGATE_LINE_RE = re.compile(r"^\s*delegate for deep dive:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
FORBIDDEN_GUARANTEE_PATTERN = re.compile(
    r"guarantee[ds]?\b.{0,30}\b(inclusion|ranking|ranked|included|placement|featured)",
    re.IGNORECASE,
)

KNOWN_DELEGATES = {
    "robots-ai-crawler-audit",
    "sitemap-discovery-audit",
    "schema-markup-audit",
    "llms-txt-generator",
    "answer-engine-content-audit",
    "citation-readiness-audit",
    "ai-search-remediation-plan",
}


@dataclass
class Finding:
    severity: str
    title: str
    body: str

    @property
    def evidence(self) -> str | None:
        match = EVIDENCE_LINE_RE.search(self.body)
        return match.group(1).strip() if match else None

    @property
    def delegate(self) -> str | None:
        match = DELEGATE_LINE_RE.search(self.body)
        return match.group(1).strip() if match else None


@dataclass
class ContractResult:
    failures: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def add(self, message: str) -> None:
        self.failures.append(message)


def parse_findings(report_text: str) -> list:
    """Split an audit report into one Finding per '- [SEVERITY] Title' bullet."""
    matches = list(FINDING_RE.finditer(report_text))
    findings = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(report_text)
        findings.append(
            Finding(severity=match.group(1).upper(), title=match.group(2).strip(),
                    body=report_text[start:end])
        )
    return findings


def check_audit_contract(
    report_text: str,
    min_findings: int = 1,
    max_findings: int | None = None,
    required_severities: list | None = None,
    required_delegates: list | None = None,
) -> ContractResult:
    """Deterministic, non-negotiable checks from SKILL.md's Output/Guardrails.

    - an "Overall: ready|partially ready|blocked" verdict line is present
    - the finding count is within [min_findings, max_findings]
    - every finding has an evidence citation and names a known delegate skill
    - no inclusion/ranking/placement guarantee language appears anywhere
    """
    result = ContractResult()

    if not OVERALL_RE.search(report_text):
        result.add("no 'Overall: ready|partially ready|blocked' verdict line found")

    findings = parse_findings(report_text)

    if len(findings) < min_findings:
        result.add(f"expected at least {min_findings} finding(s), found {len(findings)}")
    if max_findings is not None and len(findings) > max_findings:
        result.add(f"expected at most {max_findings} finding(s), found {len(findings)}")

    for finding in findings:
        if not finding.evidence:
            result.add(f"finding '{finding.title}' has no evidence citation")
        if not finding.delegate:
            result.add(f"finding '{finding.title}' names no delegate skill for deep-dive")
        elif finding.delegate not in KNOWN_DELEGATES:
            result.add(
                f"finding '{finding.title}' names delegate '{finding.delegate}' not in "
                f"SKILL.md's delegation map"
            )

    if required_severities:
        got_severities = {f.severity.lower() for f in findings}
        missing = set(s.lower() for s in required_severities) - got_severities
        if missing:
            result.add(f"missing required severity tier(s): {sorted(missing)}")

    if required_delegates:
        got_delegates = {f.delegate for f in findings if f.delegate}
        missing = set(required_delegates) - got_delegates
        if missing:
            result.add(f"missing required delegate(s): {sorted(missing)}")

    if FORBIDDEN_GUARANTEE_PATTERN.search(report_text):
        result.add(
            "report contains inclusion/ranking/placement guarantee language, which "
            "the skill's guardrails forbid"
        )

    return result


def check_decline_response(response_text: str, decline_signal_patterns: list) -> ContractResult:
    """For should-not-use scenarios: the response must not fabricate a
    finding-shaped audit report, must still respect the no-guarantee guardrail,
    and must contain at least one of the expected decline/defer signals."""
    result = ContractResult()

    if FINDING_RE.search(response_text):
        result.add(
            "response contains '- [SEVERITY] ...' finding bullets — an audit report "
            "was fabricated for an input that should have been declined or deferred"
        )

    if FORBIDDEN_GUARANTEE_PATTERN.search(response_text):
        result.add(
            "response contains inclusion/ranking/placement guarantee language, which "
            "the skill's guardrails forbid"
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

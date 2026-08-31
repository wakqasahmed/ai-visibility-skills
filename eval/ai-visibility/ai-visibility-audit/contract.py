"""Shared outcome validator for ai-visibility-audit.

Encodes the non-negotiable rules from
skills/ai-visibility/ai-visibility-audit/SKILL.md's "Output"/"Guardrails"
sections as machine-checkable functions, independent of who produced the
report being checked (a hand-authored golden fixture, or a live model
response). Both run_outcome_eval.py (deterministic, golden-fixture layer) and
model_harness.py (gated, live-model layer) import this module so the two
layers score outcomes the same way and cannot silently drift apart.

This module contains no network calls, no model calls, and no fixture-specific
logic — it only parses/scores audit-report text and decline-response text.

Note: this is a *separate* validator from the pre-existing
run_eval.py + fixture/, which hand-reimplements the commands in
skills/ai-visibility/ai-visibility-audit/references/checks.md against a
single frozen snapshot. That script proves
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

HEAD_TARGET_ABSENCE_RE = re.compile(
    r"\bno\s+(?:\w+[- ]){0,3}?(?:json-?ld|structured data|schema markup|title|meta description|"
    r"canonical(?: link| tag| url)?)\b"
    r"|\b(?:json-?ld|structured data|title|meta description|canonical(?: link| tag)?)\b"
    r"[^.\n]{0,40}?\b(?:is|are|was|were)\s*(?:absent|missing|not found|not present)\b"
    r"|\bzero\s+(?:json-?ld|structured data|schema)\b",
    re.IGNORECASE,
)
HYDRATION_CROSSCHECK_RE = re.compile(
    r"hydrated dom|rendered dom|--dump-dom|headless chrom|after (?:javascript|hydration)|"
    r"hydration cross-check",
    re.IGNORECASE,
)
NO_BROWSER_DISCLOSURE_RE = re.compile(
    r"hydration cross-check not performed|"
    r"no (?:headless |chromium-family |chromium )?browser (?:was )?available",
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


def check_hydration_crosscheck(report_text: str) -> ContractResult:
    """Issue #102: a title, meta description, canonical or JSON-LD block may exist
    only in the hydrated DOM, so a raw-HTML pass that matched nothing is unresolved,
    not absent.

    Every finding that claims one of those four is absent must therefore also say
    what the hydrated pass returned — or, when no Chromium-family browser was
    available to run one, disclose that explicitly and mark the finding [Derived]
    rather than asserting absence. Prose outside the findings is held to the same
    rule, so the claim cannot simply be moved out of a bullet.
    """
    result = ContractResult()
    findings = parse_findings(report_text)

    def verdict(scope: str, text: str) -> None:
        if not HEAD_TARGET_ABSENCE_RE.search(text):
            return
        if NO_BROWSER_DISCLOSURE_RE.search(text):
            if "[Derived]" not in text:
                result.add(
                    f"{scope} claims a title/meta/canonical/JSON-LD absence with no "
                    "hydration cross-check available, but is not labelled [Derived]"
                )
            return
        if not HYDRATION_CROSSCHECK_RE.search(text):
            result.add(
                f"{scope} claims a title/meta/canonical/JSON-LD absence from the raw "
                "response without stating what the hydrated-DOM pass returned (issue "
                "#102) — a zero-match raw pass is unresolved, not absent"
            )

    for finding in findings:
        verdict(f"finding '{finding.title}'", f"{finding.title}\n{finding.body}")

    prose = FINDING_RE.sub("", report_text)
    for finding in findings:
        prose = prose.replace(finding.body, "")
    verdict("report prose", prose)

    return result


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

    result.failures.extend(check_hydration_crosscheck(report_text).failures)

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

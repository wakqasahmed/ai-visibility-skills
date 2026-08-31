#!/usr/bin/env python3
"""Behavioral eval for the ai-visibility-audit skill.

Runs the checks documented in skills/ai-visibility/ai-visibility-audit/references/checks.md against the frozen
fixture in fixture/ (no live network calls — robots.txt and index.html are
read from disk instead of curl'd), builds a ranked findings report the same
shape the skill is expected to produce, then asserts the report satisfies
the skill's contract: known injected issues are surfaced with the right
severity tier and an evidence citation, at least one finding names its
delegate skill, and no inclusion/ranking guarantee language appears.

Exit code 0 = pass, 1 = fail.
"""
import re
import sys
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parent / "fixture"
ROBOTS_PATH = FIXTURE_DIR / "robots.txt"
PAGE_PATH = FIXTURE_DIR / "index.html"
HYDRATED_PAGE_PATH = FIXTURE_DIR / "hydrated.html"

TITLE_RE = re.compile(r"<title[^>]*>\s*[^\s<]", re.IGNORECASE)
META_DESCRIPTION_RE = re.compile(
    r'<meta[^>]+name\s*=\s*["\']?description["\'\s>][^>]*>', re.IGNORECASE
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel\s*=\s*["\']?canonical["\'\s>][^>]*>', re.IGNORECASE
)
JSON_LD_RE = re.compile(r"<script[^>]+application/ld\+json", re.IGNORECASE)

# The naive adjacent-token patterns this eval guards against: they miss any tag
# whose framework attribute (data-react-helmet, nonce, id) precedes the attribute
# being matched. Issue #102's zaavia.net false negative was exactly this.
NAIVE_META_DESCRIPTION_RE = re.compile(r'<meta name="description"', re.IGNORECASE)
NAIVE_JSON_LD_RE = re.compile(r'<script type="application/ld\+json"', re.IGNORECASE)

FORBIDDEN_GUARANTEE_PATTERN = re.compile(
    r"guarantee[ds]?\b.{0,30}\b(inclusion|ranking|ranked|included|placement)",
    re.IGNORECASE,
)


def check_robots_ai_crawler_block(robots_text: str) -> dict | None:
    """Mirrors: curl -s "$SITE/robots.txt" (references/checks.md, Discoverability)."""
    lines = robots_text.splitlines()
    blocked_agents = []
    current_agent = None
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.lower().startswith("user-agent:"):
            current_agent = stripped.split(":", 1)[1].strip()
        elif stripped.lower().startswith("disallow:") and current_agent:
            target = stripped.split(":", 1)[1].strip()
            if target == "/" and current_agent.lower() in {
                "gptbot", "claudebot", "perplexitybot", "google-extended", "ccbot",
            }:
                blocked_agents.append((current_agent, i))

    if not blocked_agents:
        return None

    agent, line_no = blocked_agents[0]
    return {
        "severity": "critical",
        "title": f"robots.txt blocks {agent} from the entire site",
        "evidence": f"robots.txt:{line_no} — \"Disallow: /\" under \"User-agent: {agent}\"",
        "delegate": "robots-ai-crawler-audit",
    }


def _no_browser_finding(label: str, delegate: str) -> dict:
    return {
        "severity": "important",
        "title": f"{label} unresolved on the representative page — no hydration cross-check possible",
        "evidence": (
            f"index.html — no {label} in the raw response; [Derived] no Chromium-family "
            "browser available, hydration cross-check not performed, so this is unresolved "
            "rather than confirmed absent"
        ),
        "delegate": delegate,
    }


def _resolve_absence(
    label: str,
    pattern: re.Pattern,
    page_html: str,
    hydrated_html: str | None,
    delegate: str,
    raw_evidence: str,
    hydrated_evidence: str,
) -> dict | None:
    """The raw+hydrated resolution SKILL.md workflow step 2 requires for all four
    targets (title, meta description, canonical, JSON-LD): a zero-match raw pass is
    unresolved, never absent, until it has been re-checked against the hydrated DOM —
    and when no browser is available to produce one, it stays unresolved and says so."""
    if pattern.search(page_html):
        return None
    if hydrated_html is None:
        return _no_browser_finding(label, delegate)
    if pattern.search(hydrated_html):
        return {
            "severity": "important",
            "title": (
                f"{label} is present in the hydrated DOM but absent from the initial "
                "server response"
            ),
            "evidence": hydrated_evidence,
            "delegate": delegate,
        }
    return {
        "severity": "important",
        "title": f"No {label} on the representative page",
        "evidence": raw_evidence,
        "delegate": delegate,
    }


def check_json_ld_delivery(page_html: str, hydrated_html: str | None) -> dict | None:
    """Mirrors references/checks.md "Machine-readable context" plus its
    "Hydrated-DOM fallback verification" section: a zero-match raw-HTML pass is
    unresolved, not absent, so it is re-checked against the hydrated DOM and the
    two results are reported as a comparison (SKILL.md workflow step 2)."""
    hydrated_count = len(JSON_LD_RE.findall(hydrated_html)) if hydrated_html else 0
    return _resolve_absence(
        "JSON-LD structured data",
        JSON_LD_RE,
        page_html,
        hydrated_html,
        "schema-markup-audit",
        raw_evidence=(
            "index.html and hydrated.html — no <script ... application/ld+json> block "
            "in the raw response or the hydrated DOM"
        ),
        hydrated_evidence=(
            "index.html — no <script ... application/ld+json> block in the raw "
            f"response; hydrated.html (chrome --headless=new --dump-dom) has "
            f"{hydrated_count} such block(s) — invisible to non-JS-executing crawlers"
        ),
    )


def check_head_metadata(page_html: str, hydrated_html: str | None) -> list[dict]:
    """Mirrors the attribute-order-tolerant title/description/canonical patterns in
    references/checks.md. Framework attributes routinely sit between the tag name and
    the attribute being matched, and the tag may only exist after hydration — so a
    zero-match raw pass goes through the same raw+hydrated resolution as JSON-LD
    before anything is called absent."""
    findings = []
    for label, pattern in (
        ("title", TITLE_RE),
        ("meta description", META_DESCRIPTION_RE),
        ("canonical link", CANONICAL_RE),
    ):
        finding = _resolve_absence(
            label,
            pattern,
            page_html,
            hydrated_html,
            "answer-engine-content-audit",
            raw_evidence=(
                f"index.html and hydrated.html — no {label} tag in the raw response or "
                "the hydrated DOM"
            ),
            hydrated_evidence=(
                f"index.html — no {label} tag in the raw response; hydrated.html "
                "(chrome --headless=new --dump-dom) has one — invisible to "
                "non-JS-executing crawlers"
            ),
        )
        if finding is not None:
            findings.append(finding)
    return findings


def check_thin_faq_content(page_html: str) -> dict | None:
    """Mirrors step 4 (answer quality / FAQs) of the SKILL.md workflow."""
    faq_match = re.search(r'<section id="faq">(.*?)</section>', page_html, re.DOTALL | re.IGNORECASE)
    if not faq_match:
        return None
    faq_body = faq_match.group(1)
    answers = re.findall(r'<p>(.*?)</p>', faq_body, re.DOTALL)
    thin_answers = [a for a in answers if len(a.strip()) < 20]
    if not thin_answers or len(thin_answers) < len(answers):
        return None
    return {
        "severity": "optional",
        "title": "FAQ answers are too thin to cite (under 20 characters each)",
        "evidence": f"index.html — FAQ section has {len(answers)} answers, all under 20 characters (e.g. \"{thin_answers[0].strip()}\")",
        "delegate": "answer-engine-content-audit",
    }


def run_audit() -> list[dict]:
    robots_text = ROBOTS_PATH.read_text()
    page_html = PAGE_PATH.read_text()
    hydrated_html = HYDRATED_PAGE_PATH.read_text()

    findings = [
        f for f in (
            check_robots_ai_crawler_block(robots_text),
            check_json_ld_delivery(page_html, hydrated_html),
            check_thin_faq_content(page_html),
        )
        if f is not None
    ]
    findings.extend(check_head_metadata(page_html, hydrated_html))

    order = {"critical": 0, "important": 1, "optional": 2}
    findings.sort(key=lambda f: order[f["severity"]])
    return findings


def render_report(findings: list[dict]) -> str:
    lines = ["# AI Visibility Audit — fixture/", ""]
    for f in findings:
        lines.append(f"- [{f['severity'].upper()}] {f['title']}")
        lines.append(f"  evidence: {f['evidence']}")
        lines.append(f"  delegate for deep dive: {f['delegate']}")
    lines.append("")
    lines.append(
        "This audit reports observed evidence only. It does not claim inclusion "
        "or ranking on any AI platform."
    )
    return "\n".join(lines)


def assert_hydration_methodology() -> list[str]:
    """Regression guard for issue #102: the two confirmed false-negative shapes —
    React-Helmet-attributed head tags, and JSON-LD that only exists after hydration —
    must not be reported as absent by a raw-HTML pass."""
    failures = []
    page_html = PAGE_PATH.read_text()
    hydrated_html = HYDRATED_PAGE_PATH.read_text()

    if NAIVE_META_DESCRIPTION_RE.search(page_html):
        failures.append(
            "fixture no longer exercises the React-Helmet case: index.html's meta "
            "description has no framework attribute before name=\"description\""
        )
    if not META_DESCRIPTION_RE.search(page_html):
        failures.append(
            "attribute-order-tolerant meta-description pattern missed a tag that is "
            "present in index.html (the zaavia.net false negative)"
        )
    reported = check_head_metadata(page_html, hydrated_html)
    if reported:
        failures.append(
            "head metadata resolvable from index.html/hydrated.html produced findings "
            f"instead of none: {[f['title'] for f in reported]}"
        )

    # The raw-absent/hydrated-present head case, which the fixture's own HTML cannot
    # express (both files carry all three tags). Each target must produce a
    # raw-vs-hydrated divergence finding, never a flat absence.
    for label, pattern in (("title", TITLE_RE), ("meta description", META_DESCRIPTION_RE),
                           ("canonical link", CANONICAL_RE)):
        stripped = pattern.sub("", page_html)
        divergent = [f for f in check_head_metadata(stripped, hydrated_html)
                     if f["title"].startswith(label)]
        if not divergent:
            failures.append(f"{label} absent from the raw pass produced no finding at all")
        elif "hydrated DOM" not in divergent[0]["title"]:
            failures.append(
                f"{label} present only in the hydrated DOM was reported as a flat absence "
                f"instead of a raw-vs-hydrated divergence: {divergent[0]['title']!r}"
            )

    # No browser at all: every zero-match raw result must be disclosed as unresolved,
    # never silently resolved to "absent" or "present".
    no_browser = check_head_metadata(TITLE_RE.sub("", page_html), None)
    no_browser.append(check_json_ld_delivery(page_html, None))
    for finding in no_browser:
        if "hydration cross-check not performed" not in finding["evidence"]:
            failures.append(
                "with no headless browser available, a zero-match raw result was not "
                f"disclosed as unresolved: {finding['title']!r}"
            )
        if "[Derived]" not in finding["evidence"]:
            failures.append(
                f"no-browser finding is not labelled [Derived]: {finding['title']!r}"
            )

    if NAIVE_JSON_LD_RE.search(page_html):
        failures.append(
            "fixture no longer exercises the hydration case: index.html itself now "
            "carries a static JSON-LD block"
        )
    if not JSON_LD_RE.search(hydrated_html):
        failures.append("hydrated.html carries no JSON-LD block to compare against")

    finding = check_json_ld_delivery(page_html, hydrated_html)
    if finding is None:
        failures.append("hydration-only JSON-LD produced no finding at all")
    elif "hydrated DOM" not in finding["title"]:
        failures.append(
            "hydration-only JSON-LD was reported as a flat absence instead of a "
            f"raw-vs-hydrated divergence: {finding['title']!r}"
        )
    return failures


def assert_report(findings: list[dict], report: str) -> list[str]:
    failures = assert_hydration_methodology()

    if len(findings) < 3:
        failures.append(f"expected >=3 injected issues surfaced, got {len(findings)}")

    expected_severities = {"critical", "important", "optional"}
    got_severities = {f["severity"] for f in findings}
    if expected_severities - got_severities:
        failures.append(
            f"missing severity tier(s): {sorted(expected_severities - got_severities)}"
        )

    for f in findings:
        if not f.get("evidence"):
            failures.append(f"finding '{f['title']}' has no evidence citation")

    # Full delegation map from SKILL.md's "## Delegation" section, so this check
    # stays valid if a future fixture case exercises a delegate this fixture
    # doesn't currently need.
    known_delegates = {
        "robots-ai-crawler-audit",
        "sitemap-discovery-audit",
        "schema-markup-audit",
        "llms-txt-generator",
        "answer-engine-content-audit",
        "citation-readiness-audit",
        "ai-search-remediation-plan",
    }
    delegates_named = {f["delegate"] for f in findings}
    if not delegates_named:
        failures.append("no finding names a delegate skill for deep-dive")
    elif not (delegates_named <= known_delegates):
        failures.append(
            f"finding names a delegate skill not in SKILL.md's delegation map: "
            f"{sorted(delegates_named - known_delegates)}"
        )

    if FORBIDDEN_GUARANTEE_PATTERN.search(report):
        failures.append("report contains inclusion/ranking guarantee language, which the skill's guardrails forbid")

    return failures


def main() -> int:
    findings = run_audit()
    report = render_report(findings)
    print(report)
    print()

    failures = assert_report(findings, report)
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS: {len(findings)} issues surfaced across {len({f['severity'] for f in findings})} severity tiers, "
          f"each with an evidence citation and a named delegate skill; no guarantee language present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

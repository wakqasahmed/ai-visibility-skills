#!/usr/bin/env python3
"""Deterministic contract layer for the robots-ai-crawler-audit skill.

Runs with no network access and no credentials. It does NOT invoke an LLM -
skills are prompt files with no code path to execute directly. Instead it
loads the hand-authored "golden" fixtures under fixtures/*/ (each one a
plausible robots.txt/header/meta-tag input plus the compliant output a
correctly-behaving agent following SKILL.md and references/checks.md would
produce) and asserts those golden outputs satisfy the skill's non-negotiable
contract, via contract.py.

This proves the fixtures and the contract checks are internally consistent
and regression-safe. It does NOT prove a live model given SKILL.md will
actually produce this exact output for a given input - that outcome-based,
skill-enabled-vs-disabled question is answered by model_harness.py, which
requires ANTHROPIC_API_KEY and is gated to a separate, non-PR workflow.

Exit code 0 = pass, 1 = fail.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract  # noqa: E402

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CHECKS_MD = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "ai-visibility"
    / "robots-ai-crawler-audit"
    / "references"
    / "checks.md"
)


def load_fixture(fixture_dir: Path) -> dict:
    meta = json.loads((fixture_dir / "meta.json").read_text())
    meta["_dir"] = fixture_dir.name
    return meta


def run_should_use_fixture(fixture_dir: Path, meta: dict) -> list:
    report_text = (fixture_dir / "golden_report.md").read_text()
    result = contract.check_audit_contract(
        report_text,
        required_patterns=meta.get("required_patterns"),
        forbidden_patterns=meta.get("forbidden_patterns"),
    )
    return result.failures


def run_should_not_use_fixture(fixture_dir: Path, meta: dict) -> list:
    response_text = (fixture_dir / "golden_response.md").read_text()
    result = contract.check_decline_response(
        response_text, meta.get("decline_signal_patterns") or []
    )
    return result.failures


def check_google_extended_probe_regression() -> list[str]:
    report = (
        FIXTURES_DIR
        / "should_use_07_experimental_content_signals_and_dns_aid"
        / "golden_report.md"
    ).read_text()
    invalid_report = report.replace(
        "for ua in GPTBot ClaudeBot PerplexityBot; do",
        "for ua in GPTBot ClaudeBot PerplexityBot Google-Extended; do",
    )
    failures = contract.check_audit_contract(invalid_report).failures
    if not any("live-probes Google-Extended" in failure for failure in failures):
        return ["contract accepted a Google-Extended HTTP user-agent probe"]
    return []


def check_citation_path_classification_regression() -> list[str]:
    report = (
        FIXTURES_DIR
        / "should_use_12_oai_searchbot_citation_block"
        / "golden_report.md"
    ).read_text()
    invalid_report = report.replace("citation-path crawler", "search crawler")
    failures = contract.check_audit_contract(invalid_report).failures
    if not any("citation-path" in failure for failure in failures):
        return [
            "contract accepted a citation-bot block without citation-path classification"
        ]
    return []


def check_citation_path_negation_regression() -> list[str]:
    """Regression check for the exact bypass the old bare-substring
    CITATION_PATH_LABEL_RE.search allowed: the literal words 'citation-path'
    appearing in a sentence that explicitly DENIES the impact ('no citation-path
    impact', 'is not a citation-path crawler') still matched the old check,
    since it only tested for the substring's presence, not whether the text
    actually affirms the classification it claims to."""
    report = (
        FIXTURES_DIR
        / "should_use_12_oai_searchbot_citation_block"
        / "golden_report.md"
    ).read_text()
    failures = []
    for negated in (
        "- OAI-SearchBot is not a citation-path crawler, so this rule prevents it from\n"
        "  indexing public pages for ChatGPT search results. Allowing GPTBot does not\n"
        "  offset this block because GPTBot is the separate training crawler.\n"
        "- Removing the block permits crawling but does not guarantee that ChatGPT will\n"
        "  index or cite any page.",
        "- There is no citation-path impact from this block. Allowing GPTBot does not\n"
        "  offset this block because GPTBot is the separate training crawler.\n"
        "- Removing the block permits crawling but does not guarantee that ChatGPT will\n"
        "  index or cite any page.",
    ):
        invalid_report = report.replace(
            "- OAI-SearchBot is OpenAI's citation-path crawler, so this rule prevents it from\n"
            "  indexing public pages for ChatGPT search results. Allowing GPTBot does not\n"
            "  offset this block because GPTBot is the separate training crawler.\n"
            "- Removing the block permits crawling but does not guarantee that ChatGPT will\n"
            "  index or cite any page.",
            negated,
        )
        assert invalid_report != report, "fixture text to replace was not found"
        result_failures = contract.check_audit_contract(invalid_report).failures
        if not any("citation-path" in failure for failure in result_failures):
            failures.append(
                f"contract accepted a report that explicitly denies citation-path "
                f"impact ({negated.splitlines()[0]!r}) as if it affirmed it"
            )
    return failures


def check_checks_md_uses_corrected_anthropic_tokens() -> list[str]:
    """Regression check that the skill's OWN instructions (references/checks.md), not
    just an eval fixture, actually name Anthropic's corrected crawler tokens and probe
    the citation-path bots live — proving a live model following this file would
    reproduce the fix, not just that a hand-edited fixture happens to satisfy the
    contract."""
    text = CHECKS_MD.read_text(encoding="utf-8")
    failures = []

    for stale_token in ("Claude-Web", "anthropic-ai"):
        if re.search(rf"\b{re.escape(stale_token)}\b", text):
            failures.append(
                f"checks.md still names the unverified/removed token '{stale_token}'"
            )

    for corrected_token in ("Claude-User", "Claude-SearchBot"):
        if not re.search(rf"\b{re.escape(corrected_token)}\b", text):
            failures.append(f"checks.md does not name the corrected token '{corrected_token}'")

    live_fetch_loops = re.findall(r"for ua in ([^;]+); do", text)
    if not any(
        "OAI-SearchBot" in loop and "Claude-SearchBot" in loop for loop in live_fetch_loops
    ):
        failures.append(
            "no live-fetch loop probes both citation-path bots (OAI-SearchBot, "
            "Claude-SearchBot) for a differential status"
        )

    return failures


def check_citation_bot_correlation_regression() -> list[str]:
    """Regression check for per-bullet bot/directive correlation: a report where one
    bullet blocks a NON-citation-path bot (GPTBot) and a SEPARATE bullet explicitly
    allows a citation-path bot (OAI-SearchBot) must not be misread as the citation-path
    bot being blocked — the old whole-section search matched CITATION_PATH_BOT_RE and
    NONEMPTY_DISALLOW_RE independently anywhere in the section, so the two unrelated
    bullets together would satisfy both and wrongly require a citation-path
    classification for OAI-SearchBot."""
    report = (
        FIXTURES_DIR
        / "should_use_12_oai_searchbot_citation_block"
        / "golden_report.md"
    ).read_text()
    mixed_report = report.replace(
        "- Every public path is blocked for OAI-SearchBot: `robots.txt` places\n"
        "  `Disallow: /` under `User-agent: OAI-SearchBot`.",
        "- `User-agent: GPTBot` has `Disallow: /`, blocking OpenAI's training crawler\n"
        "  entirely.\n"
        "- OAI-SearchBot is explicitly allowed and returns `200` on a live fetch,\n"
        "  unaffected by the GPTBot rule above.",
    ).replace(
        "- OAI-SearchBot is OpenAI's citation-path crawler, so this rule prevents it from\n"
        "  indexing public pages for ChatGPT search results. Allowing GPTBot does not\n"
        "  offset this block because GPTBot is the separate training crawler.",
        "- GPTBot is OpenAI's training crawler, so this rule stops the site's content\n"
        "  from being used to train OpenAI's models. This has no bearing on citation\n"
        "  paths, since OAI-SearchBot is unaffected and remains free to crawl.",
    )
    if mixed_report == report:
        return ["fixture text to substitute was not found — update this regression case"]
    failures = contract.check_audit_contract(mixed_report).failures
    if any("citation-path" in failure for failure in failures):
        return [
            "contract required citation-path classification for OAI-SearchBot even "
            "though only GPTBot (not a citation-path bot) is blocked in this report, "
            "and OAI-SearchBot is explicitly described as allowed"
        ]
    return []


def main() -> int:
    fixture_dirs = sorted(p for p in FIXTURES_DIR.iterdir() if p.is_dir())
    if len(fixture_dirs) < 10:
        print(f"FAIL: expected at least 10 fixtures, found {len(fixture_dirs)}")
        return 1

    should_use_count = 0
    should_not_use_count = 0
    total_failures = 0

    regression_failures = check_google_extended_probe_regression()
    status = "PASS" if not regression_failures else "FAIL"
    print(f"[{status}] contract rejects Google-Extended HTTP user-agent probes")
    for failure in regression_failures:
        print(f"    - {failure}")
        total_failures += 1

    regression_failures = check_checks_md_uses_corrected_anthropic_tokens()
    status = "PASS" if not regression_failures else "FAIL"
    print(f"[{status}] checks.md names corrected Anthropic tokens and probes citation-path bots")
    for failure in regression_failures:
        print(f"    - {failure}")
        total_failures += 1

    regression_failures = check_citation_bot_correlation_regression()
    status = "PASS" if not regression_failures else "FAIL"
    print(f"[{status}] contract correlates a citation-path bot to its own Disallow directive")
    for failure in regression_failures:
        print(f"    - {failure}")
        total_failures += 1

    regression_failures = check_citation_path_classification_regression()
    status = "PASS" if not regression_failures else "FAIL"
    print(f"[{status}] contract requires citation-path classification for citation-bot blocks")
    for failure in regression_failures:
        print(f"    - {failure}")
        total_failures += 1

    regression_failures = check_citation_path_negation_regression()
    status = "PASS" if not regression_failures else "FAIL"
    print(f"[{status}] contract rejects negated citation-path classifications")
    for failure in regression_failures:
        print(f"    - {failure}")
        total_failures += 1

    for fixture_dir in fixture_dirs:
        meta = load_fixture(fixture_dir)
        category = meta["category"]

        if category == "should_use":
            should_use_count += 1
            failures = run_should_use_fixture(fixture_dir, meta)
        elif category == "should_not_use":
            should_not_use_count += 1
            failures = run_should_not_use_fixture(fixture_dir, meta)
        else:
            failures = [f"unknown category '{category}'"]

        status = "PASS" if not failures else "FAIL"
        print(f"[{status}] {fixture_dir.name} ({category})")
        for failure in failures:
            print(f"    - {failure}")
            total_failures += 1

    print()
    if should_use_count < 5:
        print(f"FAIL: expected at least 5 should_use fixtures, found {should_use_count}")
        total_failures += 1
    if should_not_use_count < 5:
        print(f"FAIL: expected at least 5 should_not_use fixtures, found {should_not_use_count}")
        total_failures += 1

    if total_failures:
        print(f"\nFAIL: {total_failures} contract violation(s) across {len(fixture_dirs)} fixtures")
        return 1

    print(
        f"\nPASS: {len(fixture_dirs)} fixtures ({should_use_count} should_use, "
        f"{should_not_use_count} should_not_use) all satisfy the deterministic contract"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

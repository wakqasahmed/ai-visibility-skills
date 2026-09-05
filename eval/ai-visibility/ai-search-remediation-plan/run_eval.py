#!/usr/bin/env python3
"""Deterministic contract layer for the ai-search-remediation-plan skill.

Runs with no network access and no credentials. It does NOT invoke an LLM —
skills are prompt files with no code path to execute directly. Instead it
loads the hand-authored "golden" fixtures under fixtures/*/ (each one a
plausible audit-finding input plus the compliant output a correctly-behaving
agent following SKILL.md and references/checks.md would produce) and asserts
those golden outputs satisfy the skill's non-negotiable contract, via
contract.py.

This proves the fixtures and the contract checks are internally consistent
and regression-safe. It does NOT prove a live model given SKILL.md will
actually produce this exact output for a given input — that outcome-based,
skill-enabled-vs-disabled question is answered by model_harness.py, which
requires ANTHROPIC_API_KEY and is gated to a separate, non-PR workflow.

Exit code 0 = pass, 1 = fail.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract  # noqa: E402

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def load_fixture(fixture_dir: Path) -> dict:
    meta = json.loads((fixture_dir / "meta.json").read_text())
    meta["_dir"] = fixture_dir.name
    return meta


def run_should_use_fixture(fixture_dir: Path, meta: dict) -> list:
    plan_text = (fixture_dir / "golden_plan.md").read_text()
    result = contract.check_plan_contract(
        plan_text, expected_ticket_count=meta.get("expected_ticket_count")
    )
    blocked_titles = meta.get("expected_blocked_ticket_titles") or []
    if blocked_titles:
        blocked_result = contract.check_blocked_tickets_present(plan_text, blocked_titles)
        result.failures.extend(blocked_result.failures)
    return result.failures


def run_should_not_use_fixture(fixture_dir: Path, meta: dict) -> list:
    response_text = (fixture_dir / "golden_response.md").read_text()
    result = contract.check_decline_response(
        response_text, meta.get("decline_signal_patterns") or []
    )
    return result.failures


def assert_per_ticket_priority_is_enforced() -> list:
    """Regression check for the per-ticket P0-P3 label requirement: a plan that
    declares the full priority vocabulary once at the top, but omits a priority
    label from an individual ticket's own body, must fail the contract. Proves
    the negative — this exact input passed against contract.py before the
    per-ticket check was added, since only the whole-document vocabulary was
    checked, not each ticket."""
    plan_missing_ticket_priority = (
        "**Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), "
        "P3 (Optional/Experimental) backlog.\n\n"
        "## Unblock GPTBot in robots.txt\n\n"
        "- Evidence Tier: Tier 1 — Critical Foundation\n"
        "- Source finding: robots-ai-crawler-audit, robots.txt:4\n"
        "- Acceptance criteria: `robots.txt` no longer contains `Disallow: /` "
        "under `User-agent: GPTBot`.\n"
        "- Verification:\n"
        "  ```bash\n"
        '  curl -s -o /dev/null -w "%{http_code}\\n" -A "GPTBot" "$URL"\n'
        "  ```\n"
        "- Owner: engineering.\n"
    )
    result = contract.check_plan_contract(plan_missing_ticket_priority, expected_ticket_count=1)
    failures = []
    if result.passed:
        failures.append(
            "check_plan_contract did not reject a ticket with no priority label of "
            "its own, even though the plan declares the full P0-P3 vocabulary once "
            "elsewhere — the per-ticket priority requirement is not enforced"
        )

    plan_non_standard_priority_with_coincidental_prose = (
        "**Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), "
        "P3 (Optional/Experimental) backlog.\n\n"
        "## Unblock GPTBot in robots.txt\n\n"
        "- Priority: urgent\n"
        "- Evidence Tier: Tier 1 — Critical Foundation\n"
        "- Source finding: robots-ai-crawler-audit, robots.txt:4\n"
        "- Acceptance criteria: `robots.txt` no longer contains `Disallow: /` "
        "under `User-agent: GPTBot`.\n"
        "- Owner: schedule this as P0 (Immediate) given crawler impact.\n"
        "- Verification:\n"
        "  ```bash\n"
        '  curl -s -o /dev/null -w "%{http_code}\\n" -A "GPTBot" "$URL"\n'
        "  ```\n"
    )
    result = contract.check_plan_contract(
        plan_non_standard_priority_with_coincidental_prose, expected_ticket_count=1
    )
    if result.passed:
        failures.append(
            "check_plan_contract accepted a ticket whose own '- Priority:' field "
            "declares a non-standard value ('urgent') merely because a canonical "
            "label's text ('P0 (Immediate)') also happens to appear elsewhere in "
            "the ticket's prose — the priority check is matching by substring "
            "instead of parsing the declared field"
        )
    return failures


def main() -> int:
    fixture_dirs = sorted(p for p in FIXTURES_DIR.iterdir() if p.is_dir())
    if len(fixture_dirs) < 10:
        print(f"FAIL: expected at least 10 fixtures, found {len(fixture_dirs)}")
        return 1

    should_use_count = 0
    should_not_use_count = 0
    total_failures = 0

    regression_failures = assert_per_ticket_priority_is_enforced()
    if regression_failures:
        print("[FAIL] per_ticket_priority_regression")
        for failure in regression_failures:
            print(f"    - {failure}")
            total_failures += 1
    else:
        print("[PASS] per_ticket_priority_regression")

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

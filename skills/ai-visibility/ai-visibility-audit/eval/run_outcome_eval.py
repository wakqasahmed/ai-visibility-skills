#!/usr/bin/env python3
"""Deterministic outcome-contract layer for the ai-visibility-audit skill (issue #21).

Runs with no network access and no credentials. It does NOT invoke an LLM —
skills are prompt files with no code path to execute directly. Instead it
loads the hand-authored "golden" fixtures under fixtures/*/ (each one a
plausible site-audit input plus the compliant output a correctly-behaving
agent following SKILL.md would produce) and asserts those golden outputs
satisfy the skill's outcome contract, via contract.py.

This proves the fixtures and the contract checks are internally consistent
and regression-safe. It does NOT prove a live model given SKILL.md will
actually produce this exact output for a given input — that outcome-based,
skill-enabled-vs-disabled question is answered by model_harness.py, which
requires ANTHROPIC_API_KEY and is gated to a separate, non-PR workflow.

This is a separate, broader layer from the pre-existing run_eval.py +
fixture/, which hand-reimplements the commands in references/checks.md
against one frozen snapshot. Both are kept and both run in CI.

Exit code 0 = pass, 1 = fail.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract  # noqa: E402

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def load_meta(fixture_dir: Path) -> dict:
    meta = json.loads((fixture_dir / "meta.json").read_text())
    meta["_dir"] = fixture_dir.name
    return meta


def run_audit_fixture(fixture_dir: Path, meta: dict) -> list:
    report_text = (fixture_dir / "golden_report.md").read_text()
    result = contract.check_audit_contract(
        report_text,
        min_findings=meta.get("expected_min_findings", 1),
        max_findings=meta.get("expected_max_findings"),
        required_severities=meta.get("expected_severities") or None,
        required_delegates=meta.get("expected_delegates") or None,
    )
    return result.failures


def run_decline_fixture(fixture_dir: Path, meta: dict) -> list:
    response_text = (fixture_dir / "golden_response.md").read_text()
    result = contract.check_decline_response(
        response_text, meta.get("decline_signal_patterns") or []
    )
    return result.failures


def main() -> int:
    fixture_dirs = sorted(p for p in FIXTURES_DIR.iterdir() if p.is_dir())
    if len(fixture_dirs) < 10:
        print(f"FAIL: expected at least 10 fixtures, found {len(fixture_dirs)}")
        return 1

    should_use_count = 0
    should_not_use_count = 0
    total_failures = 0

    for fixture_dir in fixture_dirs:
        meta = load_meta(fixture_dir)
        category = meta["category"]
        mode = meta["mode"]

        if category == "should_use":
            should_use_count += 1
        elif category == "should_not_use":
            should_not_use_count += 1

        if mode == "audit":
            failures = run_audit_fixture(fixture_dir, meta)
        elif mode == "decline":
            failures = run_decline_fixture(fixture_dir, meta)
        else:
            failures = [f"unknown mode '{mode}'"]

        status = "PASS" if not failures else "FAIL"
        print(f"[{status}] {fixture_dir.name} ({category}/{mode})")
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
        f"{should_not_use_count} should_not_use) all satisfy the deterministic outcome contract"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

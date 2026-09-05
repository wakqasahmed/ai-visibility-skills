#!/usr/bin/env python3
"""Deterministic contract layer for the sitemap-discovery-audit skill.

Runs with no network access and no credentials. It does NOT invoke an LLM —
skills are prompt files with no code path to execute directly. Instead it
loads the hand-authored "golden" fixtures under fixtures/*/ (each one a
plausible user request plus the compliant output a correctly-behaving agent
following SKILL.md and references/checks.md would produce) and asserts those
golden outputs satisfy the skill's non-negotiable contract, via contract.py.

This proves the fixtures and the contract checks are internally consistent
and regression-safe. It does NOT prove a live model given SKILL.md will
actually produce this exact output for a given input — that outcome-based,
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
    / "sitemap-discovery-audit"
    / "references"
    / "checks.md"
)
BASH_FENCE_RE = re.compile(r"```bash\n(.*?)\n```", re.DOTALL)


def assert_work_scratch_dir_stays_in_scope() -> list:
    """Regression check for the /tmp scratch-dir collision fix: every fenced bash
    block that reads or writes `"$WORK"/...` must itself contain the `WORK=$(mktemp
    -d)` assignment, since each ```bash fence is a separately-invoked shell and a
    variable set in one does not carry over into the next. A block that uses
    `$WORK` without setting it would silently resolve to a bare filename in the
    current directory instead of the scratch directory — this exact bug existed
    before the fix, split across two separate fenced blocks."""
    checks_text = CHECKS_MD.read_text(encoding="utf-8")
    failures = []
    for index, block in enumerate(BASH_FENCE_RE.findall(checks_text), start=1):
        uses_work = "$WORK" in block
        sets_work = "WORK=$(mktemp" in block
        if uses_work and not sets_work:
            failures.append(
                f"checks.md bash block #{index} references \"$WORK\" but does not "
                f"assign WORK=$(mktemp -d) in the same block — it would run as a "
                f"separate shell invocation with WORK unset"
            )
    return failures


def load_fixture(fixture_dir: Path) -> dict:
    meta = json.loads((fixture_dir / "meta.json").read_text())
    meta["_dir"] = fixture_dir.name
    return meta


def run_should_use_fixture(fixture_dir: Path, meta: dict) -> list:
    report_text = (fixture_dir / "golden_report.md").read_text()
    result = contract.check_report_contract(report_text, meta)
    return result.failures


def run_should_not_use_fixture(fixture_dir: Path, meta: dict) -> list:
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

    scratch_dir_failures = assert_work_scratch_dir_stays_in_scope()
    if scratch_dir_failures:
        print("[FAIL] work_scratch_dir_scope_regression")
        for failure in scratch_dir_failures:
            print(f"    - {failure}")
            total_failures += 1
    else:
        print("[PASS] work_scratch_dir_scope_regression")

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

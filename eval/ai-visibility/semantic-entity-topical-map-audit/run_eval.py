#!/usr/bin/env python3
"""Deterministic evaluation runner for semantic-entity-topical-map-audit."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from contract import validate_decline_contract, validate_report_contract

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CHECKS_MD = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "ai-visibility"
    / "semantic-entity-topical-map-audit"
    / "references"
    / "checks.md"
)
BASH_FENCE_RE = re.compile(r"```bash\n(.*?)\n```", re.DOTALL)


def assert_work_scratch_dir_stays_in_scope() -> list:
    """Regression check for the /tmp scratch-dir collision fix: every fenced bash
    block that reads or writes `"$WORK"/...` must itself contain the `WORK=$(mktemp
    -d)` assignment, since each ```bash fence is a separately-invoked shell and a
    variable set in one does not carry over into the next."""
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


def run_eval() -> int:
    fixtures = sorted([d for d in FIXTURES_DIR.iterdir() if d.is_dir()])
    if not fixtures:
        print("FAIL: No fixtures found in", FIXTURES_DIR)
        return 1

    total = len(fixtures) + 1
    passed = 0
    failures = []

    scratch_dir_failures = assert_work_scratch_dir_stays_in_scope()
    if scratch_dir_failures:
        failures.append(("work_scratch_dir_scope_regression", "; ".join(scratch_dir_failures)))
        print(f"  [FAIL] work_scratch_dir_scope_regression: {'; '.join(scratch_dir_failures)}")
    else:
        passed += 1
        print("  [PASS] work_scratch_dir_scope_regression")

    for fix in fixtures:
        meta_path = fix / "meta.json"
        if not meta_path.exists():
            failures.append((fix.name, "missing meta.json"))
            continue

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append((fix.name, f"invalid meta.json: {exc}"))
            continue
        fix_type = meta.get("type", "should_use")

        if fix_type == "should_use":
            report_file = fix / "golden_report.md"
            if not report_file.exists():
                failures.append((fix.name, "missing golden_report.md"))
                continue
            text = report_file.read_text(encoding="utf-8")
            res = validate_report_contract(text)
        else:
            response_file = fix / "golden_response.md"
            if not response_file.exists():
                failures.append((fix.name, "missing golden_response.md"))
                continue
            text = response_file.read_text(encoding="utf-8")
            res = validate_decline_contract(text)

        if res.passed:
            passed += 1
            print(f"  [PASS] {fix.name}")
        else:
            failures.append((fix.name, "; ".join(res.failures)))
            print(f"  [FAIL] {fix.name}: {'; '.join(res.failures)}")

    print(f"\nResult: {passed}/{total} fixtures passed.")
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_eval())

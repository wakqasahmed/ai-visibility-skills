#!/usr/bin/env python3
"""Deterministic evaluation runner for ai-share-of-voice-audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from contract import validate_decline_contract, validate_report_contract

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def run_eval() -> int:
    fixtures = sorted([d for d in FIXTURES_DIR.iterdir() if d.is_dir()])
    if not fixtures:
        print("FAIL: No fixtures found in", FIXTURES_DIR)
        return 1

    total = len(fixtures)
    passed = 0
    failures = []

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

#!/usr/bin/env python3
"""Deterministic evaluation runner for indexnow-instant-indexing-audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from contract import validate_decline_contract, validate_report_contract

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
REJECT_DIR = Path(__file__).resolve().parent / "contract_negatives"


def _read(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeDecodeError) as exc:
        return None, f"cannot read {path.name}: {exc}"


def _load_meta(fix: Path) -> tuple[dict | None, str | None]:
    meta_path = fix / "meta.json"
    if not meta_path.exists():
        return None, "missing meta.json"
    try:
        return json.loads(meta_path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"invalid meta.json: {exc}"


def _list_dirs(root: Path) -> tuple[list[Path], str | None]:
    try:
        return sorted([d for d in root.iterdir() if d.is_dir()]), None
    except OSError as exc:
        return [], f"unable to read directory {root}: {exc}"


def run_eval() -> int:
    fixtures, err = _list_dirs(FIXTURES_DIR)
    if err:
        print("FAIL:", err)
        return 1
    if not fixtures:
        print("FAIL: No fixtures found in", FIXTURES_DIR)
        return 1

    passed = 0
    failures = []

    for fix in fixtures:
        meta, err = _load_meta(fix)
        if err:
            failures.append((fix.name, err))
            print(f"  [FAIL] {fix.name}: {err}")
            continue

        fix_type = meta.get("type", "should_use")
        golden = fix / ("golden_report.md" if fix_type == "should_use" else "golden_response.md")
        if not golden.exists():
            failures.append((fix.name, f"missing {golden.name}"))
            print(f"  [FAIL] {fix.name}: missing {golden.name}")
            continue

        text, err = _read(golden)
        if err:
            failures.append((fix.name, err))
            print(f"  [FAIL] {fix.name}: {err}")
            continue

        validate = validate_report_contract if fix_type == "should_use" else validate_decline_contract
        res = validate(text)

        if res.passed:
            passed += 1
            print(f"  [PASS] {fix.name}")
        else:
            failures.append((fix.name, "; ".join(res.failures)))
            print(f"  [FAIL] {fix.name}: {'; '.join(res.failures)}")

    print(f"\nGolden fixtures: {passed}/{len(fixtures)} passed.")

    rejected, reject_failures = run_reject_eval()
    if reject_failures:
        failures.extend(reject_failures)

    print(f"Contract negatives: {rejected} rejected as expected.")
    return 1 if failures else 0


def run_reject_eval() -> tuple[int, list[tuple[str, str]]]:
    """Held-out negatives: responses the contract must REJECT.

    Without these the golden-only suite is tautological - every validator failure branch
    would be unexercised, so a regression in the contract would go undetected.
    """
    cases, err = _list_dirs(REJECT_DIR)
    if err:
        return 0, [("contract_negatives", err)]

    rejected = 0
    failures = []
    for case in cases:
        meta, err = _load_meta(case)
        if err:
            failures.append((case.name, err))
            print(f"  [FAIL] {case.name}: {err}")
            continue

        fix_type = meta.get("type", "should_use")
        candidate = case / "response.md"
        text, err = _read(candidate)
        if err:
            failures.append((case.name, err))
            print(f"  [FAIL] {case.name}: {err}")
            continue

        validate = validate_report_contract if fix_type == "should_use" else validate_decline_contract
        res = validate(text)

        if res.passed:
            reason = f"contract accepted a response it must reject ({meta.get('rejects', 'unspecified')})"
            failures.append((case.name, reason))
            print(f"  [FAIL] {case.name}: {reason}")
        else:
            rejected += 1
            print(f"  [PASS] {case.name} (rejected: {'; '.join(res.failures)})")

    return rejected, failures


if __name__ == "__main__":
    sys.exit(run_eval())

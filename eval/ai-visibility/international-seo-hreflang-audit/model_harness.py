"""Live model evaluation harness for international-seo-hreflang-audit."""
from __future__ import annotations

import json
from pathlib import Path
from contract import validate_decline_contract, validate_report_contract

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def evaluate_response(fixture_name: str, response_text: str) -> dict:
    meta_file = FIXTURES_DIR / fixture_name / "meta.json"
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    if meta.get("type") == "should_use":
        res = validate_report_contract(response_text)
    else:
        res = validate_decline_contract(response_text)
    return {"passed": res.passed, "failures": res.failures}

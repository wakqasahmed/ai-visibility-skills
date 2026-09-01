"""Live model evaluation harness for semantic-entity-topical-map-audit."""
from __future__ import annotations

import json
from pathlib import Path

from contract import validate_decline_contract, validate_report_contract

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SKILL_MD = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "ai-visibility"
    / "semantic-entity-topical-map-audit"
    / "SKILL.md"
)


def get_system_prompt() -> str:
    if not SKILL_MD.exists():
        raise FileNotFoundError(f"Missing SKILL.md at {SKILL_MD}")
    return SKILL_MD.read_text(encoding="utf-8")


def evaluate_response(fixture_name: str, response_text: str) -> dict:
    meta_file = FIXTURES_DIR / fixture_name / "meta.json"
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"passed": False, "failures": [f"invalid meta.json: {exc}"]}
    # Default must match run_eval.py's, or a fixture missing "type" would be graded
    # as a report deterministically and as a decline live.
    if meta.get("type", "should_use") == "should_use":
        res = validate_report_contract(response_text)
    else:
        res = validate_decline_contract(response_text)
    return {"passed": res.passed, "failures": res.failures}

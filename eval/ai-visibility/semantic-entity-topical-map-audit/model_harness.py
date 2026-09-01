"""Model harness for semantic-entity-topical-map-audit."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_MD = Path(__file__).resolve().parents[3] / "skills" / "ai-visibility" / "semantic-entity-topical-map-audit" / "SKILL.md"


def get_system_prompt() -> str:
    if not SKILL_MD.exists():
        raise FileNotFoundError(f"Missing SKILL.md at {SKILL_MD}")
    return SKILL_MD.read_text(encoding="utf-8")

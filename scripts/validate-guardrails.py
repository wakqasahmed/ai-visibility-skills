#!/usr/bin/env python3
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
canonical_path = root / "skills" / "ai-visibility" / "references" / "guardrails.md"
canonical = canonical_path.read_bytes()
errors = []
copies = []

for skill_path in sorted(root.glob("skills/ai-visibility/*/SKILL.md")):
    if "references/guardrails.md" not in skill_path.read_text():
        continue
    copy_path = skill_path.parent / "references" / "guardrails.md"
    copies.append(copy_path)
    if not copy_path.is_file():
        errors.append(f"missing per-skill guardrail copy: {copy_path.relative_to(root)}")
    elif copy_path.read_bytes() != canonical:
        errors.append(f"guardrail copy differs from canonical: {copy_path.relative_to(root)}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)

print(f"validated {len(copies)} per-skill guardrail copies")

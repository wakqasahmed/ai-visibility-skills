#!/usr/bin/env python3
import datetime
import os
import re
import sys
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
warnings = []

index = json.loads((root / "SOURCE_INDEX.json").read_text())
sources_text = (root / "SOURCES.md").read_text()
table_ids = set(re.findall(r"^\| `([A-Z0-9-]+)` \|", sources_text, re.M))

if set(index) != table_ids:
    errors.append(
        f"SOURCE_INDEX.json and SOURCES.md disagree: only in index {sorted(set(index) - table_ids)}, "
        f"only in table {sorted(table_ids - set(index))}"
    )

# This repo nests skills under skills/ai-visibility/<name>/ rather than skills/<name>/,
# and concrete crawler/schema claims often live in each skill's references/checks.md
# rather than its SKILL.md, so both are scanned for citations.
citable_files = sorted(root.glob("skills/ai-visibility/*/SKILL.md")) + sorted(
    root.glob("skills/ai-visibility/*/references/*.md")
)

used = set()
for path in citable_files:
    unregistered = set()
    for cite in re.findall(r"\[([A-Z][A-Z0-9-]*-\d+)\]", path.read_text()):
        used.add(cite)
        if cite not in index:
            unregistered.add(cite)
    for cite in sorted(unregistered):
        errors.append(f"{path.relative_to(root)} cites unregistered ID [{cite}]")

unused = sorted(set(index) - used)
if unused:
    errors.append(f"registered but never cited: {unused}")

today = datetime.date.today()
match = re.search(r"^Last reviewed: (\d{4}-\d{2}-\d{2})$", sources_text, re.M)
if not match:
    errors.append("SOURCES.md has no 'Last reviewed:' date")
else:
    age = (today - datetime.date.fromisoformat(match.group(1))).days
    if age > 180:
        warnings.append(f"SOURCES.md last reviewed {age} days ago; re-verify its sources")

for warning in warnings:
    prefix = "::warning::" if os.environ.get("GITHUB_ACTIONS") else "WARNING: "
    print(f"{prefix}{warning}")
if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)

print(f"validated {len(used)} cited source IDs across {len(citable_files)} files")

#!/usr/bin/env python3
"""Regression check for issue #126: fixed, generically-named /tmp scratch
files (`/tmp/sitemap-urls.txt`, `/tmp/nav-links.txt`, `/tmp/hydrated.html`,
etc.) written by more than one skill's checks.md collide within a single
orchestrated session (the orchestrator runs specialist skills in the same
agent session, so a fixed path from one skill silently clobbers or is
clobbered by another before its own diff/read runs).

The fix is a per-run `WORK=$(mktemp -d)` scratch dir plus a skill-specific
filename prefix inside it. This validator enforces both invariants across
every skill's checks.md, not just the two skills that happened to get their
own regression test first:

1. No bash fence in any checks.md hardcodes a well-known /tmp path.
2. Every fence that reads or writes "$WORK"/... also assigns
   WORK=$(mktemp -d) in that same fence, since each ```bash fence is a
   separately-invoked shell and a variable set in one does not carry over
   into the next.
3. No two different skills use the exact same filename under "$WORK", so a
   same-named file from a different skill's scratch dir cannot be mistaken
   for this skill's data even if the skills ever shared a scratch dir.
"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
skills_dir = root / "skills" / "ai-visibility"
checks_files = sorted(skills_dir.glob("*/references/checks.md"))

BASH_FENCE_RE = re.compile(r"```bash\n(.*?)\n```", re.DOTALL)
WORK_FILE_RE = re.compile(r'"\$WORK"/(\S+?)(?=["\s)])')
KNOWN_COLLIDING_NAMES = {
    "sitemap-urls.txt",
    "nav-links.txt",
    "hydrated.html",
}

errors = []
work_filenames_by_skill: dict[str, set[str]] = {}

for checks_md in checks_files:
    skill_name = checks_md.parents[1].name
    text = checks_md.read_text(encoding="utf-8")

    for name in KNOWN_COLLIDING_NAMES:
        if re.search(rf"/tmp/{re.escape(name)}\b", text):
            errors.append(f"{checks_md}: hardcodes the known-colliding path /tmp/{name}")

    skill_filenames = work_filenames_by_skill.setdefault(skill_name, set())
    for index, block in enumerate(BASH_FENCE_RE.findall(text), start=1):
        uses_work = "$WORK" in block
        sets_work = "WORK=$(mktemp" in block
        if uses_work and not sets_work:
            errors.append(
                f"{checks_md}: bash block #{index} references \"$WORK\" but does not "
                f"assign WORK=$(mktemp -d) in the same block — it would run as a "
                f"separate shell invocation with WORK unset"
            )
        for filename in WORK_FILE_RE.findall(block):
            skill_filenames.add(filename.rstrip(","))

# Cross-skill filename uniqueness: a filename reused by two different skills
# under "$WORK" is exactly the collision this validator exists to catch, even
# though each skill's own mktemp -d normally makes that dir unique — a shared
# host, an orchestrator that ever pools scratch space, or a future refactor
# could still make two skills' filenames land in the same directory.
seen: dict[str, str] = {}
for skill_name, filenames in work_filenames_by_skill.items():
    for filename in filenames:
        if filename in seen and seen[filename] != skill_name:
            errors.append(
                f"filename {filename!r} under \"$WORK\" is used by both "
                f"{seen[filename]!r} and {skill_name!r} — not skill-specific"
            )
        else:
            seen[filename] = skill_name

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)

print(f"validated scratch-dir isolation across {len(checks_files)} checks.md files")

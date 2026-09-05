#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def _unquote(token: str) -> str:
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "'\"":
        return token[1:-1]
    return token


FULL_SHA = re.compile(r"[0-9a-f]{40}")
# The `uses`/`permissions` mapping keys accept an optional matching pair of quotes in
# YAML (`'uses': x` and `uses: x` are the same key) — match both, so a quoted key
# cannot silently bypass the checks below the way an unquoted-only pattern would.
USES = re.compile(r"^\s*(?:-\s+)?(['\"]?)uses\1:\s*([^\s#]+)", re.MULTILINE)
PERMISSIONS = re.compile(
    r"^(?P<indent>\s*)(['\"]?)permissions\2:\s*(?P<value>[^#]*?)\s*(?:#.*)?$"
)
PERMISSION_ENTRY = re.compile(
    r"^\s+(['\"]?)([a-z-]+)\1:\s*(['\"]?)(read|write|none)\3\s*(?:#.*)?$"
)
ALLOWED_WRITE_PERMISSIONS = {
    "ocr-manual-review.yml": {"issues", "pull-requests"},
    "open-code-review.yml": {"pull-requests"},
}


def permission_blocks(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    blocks = []
    for index, line in enumerate(lines):
        match = PERMISSIONS.match(line)
        if not match:
            continue
        if match.group("value"):
            blocks.append({"*": _unquote(match.group("value"))})
            continue

        indent = len(match.group("indent"))
        block = {}
        for entry_line in lines[index + 1 :]:
            if not entry_line.strip() or entry_line.lstrip().startswith("#"):
                continue
            entry_indent = len(entry_line) - len(entry_line.lstrip())
            if entry_indent <= indent:
                break
            entry = PERMISSION_ENTRY.match(entry_line)
            if entry:
                block[entry.group(2)] = entry.group(4)
        blocks.append(block)
    return blocks


root = Path(__file__).resolve().parents[1]
workflows_dir = root / ".github" / "workflows"
workflow_paths = sorted((*workflows_dir.glob("*.yml"), *workflows_dir.glob("*.yaml")))
errors = []
action_count = 0

for path in workflow_paths:
    relative_path = path.relative_to(root)
    text = path.read_text()

    for raw_action in USES.findall(text):
        action = _unquote(raw_action[1])
        if action.startswith("./"):
            continue
        action_count += 1
        if "@" not in action or not FULL_SHA.fullmatch(action.rsplit("@", 1)[1]):
            errors.append(f"{relative_path}: action is not pinned to a full SHA: {action}")

    blocks = permission_blocks(text)
    allowed_writes = ALLOWED_WRITE_PERMISSIONS.get(path.name, set())
    for block in blocks:
        if "*" in block:
            if block["*"] not in {"{}", "read-all"}:
                errors.append(f"{relative_path}: unsupported or writable inline permissions")
            continue
        for permission, access in block.items():
            if access == "write" and permission not in allowed_writes:
                errors.append(f"{relative_path}: unexpected write permission: {permission}")

    if path.name.endswith("-model-eval.yml") and blocks != [{"contents": "read"}]:
        errors.append(f"{relative_path}: model eval permissions must be contents: read only")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)

print(f"validated {action_count} pinned action references across {len(workflow_paths)} workflows")

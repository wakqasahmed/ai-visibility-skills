#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def normalize_plugin_paths(paths: list[str]) -> tuple[list[str], list[str]]:
    names = []
    errors = []
    for raw_path in paths:
        if not isinstance(raw_path, str):
            errors.append(f"plugin skill path is not a string: {raw_path!r}")
            continue
        path = Path(raw_path)
        if path.is_absolute() or len(path.parts) != 3 or path.parts[0:2] != ("skills", "ai-visibility"):
            errors.append(f"invalid plugin skill path: {raw_path}")
            continue
        names.append(path.parts[2])
    return names, errors


def registry_errors(
    actual_names: list[str], plugin_paths: list[str], manifest_names: list[str]
) -> list[str]:
    plugin_names, errors = normalize_plugin_paths(plugin_paths)
    expected = sorted(actual_names)

    duplicate_plugin_names = duplicates(plugin_names)
    if duplicate_plugin_names:
        errors.append("duplicate plugin skills: " + ", ".join(duplicate_plugin_names))

    duplicate_manifest_names = duplicates(manifest_names)
    if duplicate_manifest_names:
        errors.append("duplicate manifest skills: " + ", ".join(duplicate_manifest_names))

    if sorted(plugin_names) != expected:
        errors.append(f"plugin skills {plugin_names} do not match actual skills {expected}")
    if sorted(manifest_names) != expected:
        errors.append(f"manifest skills {manifest_names} do not match actual skills {expected}")
    return errors


def synchronization_errors(root: Path, skill_names: list[str]) -> list[str]:
    errors = []
    canonical_guardrails = root / "skills/ai-visibility/references/guardrails.md"
    canonical_guardrails_bytes = canonical_guardrails.read_bytes()

    for skill_name in skill_names:
        bundled_guardrails = root / "skills/ai-visibility" / skill_name / "references/guardrails.md"
        if not bundled_guardrails.is_file():
            errors.append(f"missing shared guardrails copy: {bundled_guardrails.relative_to(root)}")
        elif bundled_guardrails.read_bytes() != canonical_guardrails_bytes:
            errors.append(f"shared guardrails copy is out of sync: {bundled_guardrails.relative_to(root)}")

    synchronized_documents = [
        (
            root / "docs/SCORING_RUBRIC.md",
            root / "skills/ai-visibility/ai-visibility-audit/references/scoring_rubric.md",
            {
                "(templates/AUDIT_REPORT_TEMPLATE_V3.md)": "(audit_report_template_v3.md)",
            },
        ),
        (
            root / "docs/templates/AUDIT_REPORT_TEMPLATE_V3.md",
            root / "skills/ai-visibility/ai-visibility-audit/references/audit_report_template_v3.md",
            {
                "(../SCORING_RUBRIC.md)": "(scoring_rubric.md)",
            },
        ),
    ]

    for canonical, bundled, link_rewrites in synchronized_documents:
        expected = canonical.read_text()
        for canonical_link, bundled_link in link_rewrites.items():
            if canonical_link not in expected:
                errors.append(f"documented link rewrite is missing from {canonical.relative_to(root)}: {canonical_link}")
            expected = expected.replace(canonical_link, bundled_link)
        if bundled.read_text() != expected:
            errors.append(f"bundled document is out of sync: {bundled.relative_to(root)}")

    return errors


root = Path(__file__).resolve().parents[1]
plugin = json.loads((root / ".claude-plugin" / "plugin.json").read_text())
skills = plugin.get("skills", [])
manifest = json.loads((root / "manifest.json").read_text())
manifest_skills = manifest.get("skills", [])
actual_skills = sorted(path.parent.name for path in root.glob("skills/ai-visibility/*/SKILL.md"))

errors = registry_errors(actual_skills, skills, manifest_skills)
if errors:
    raise SystemExit("Skill registry mismatch: " + "; ".join(errors))

errors = synchronization_errors(root, actual_skills)
if errors:
    raise SystemExit("Synchronized copy mismatch: " + "; ".join(errors))

missing = [skill for skill in skills if not (root / skill / "SKILL.md").is_file()]
if missing:
    raise SystemExit("Missing plugin skill paths: " + ", ".join(missing))

for skill in skills:
    path = root / skill
    name_line = next(
        (line for line in (path / "SKILL.md").read_text().splitlines() if line.startswith("name: ")),
        None,
    )
    if name_line != f"name: {path.name}":
        raise SystemExit(f"Skill name does not match its directory: {path}")

if manifest.get("skill_count") != len(actual_skills):
    raise SystemExit(f"manifest.json skill_count is {manifest.get('skill_count')}, repo has {len(actual_skills)}")

source_index_path = root / "SOURCE_INDEX.json"
if source_index_path.is_file():
    source_index = json.loads(source_index_path.read_text())
    if manifest.get("source_count") != len(source_index):
        raise SystemExit(f"manifest.json source_count is {manifest.get('source_count')}, registry has {len(source_index)}")
elif manifest.get("source_count") != 0:
    raise SystemExit("manifest.json source_count is set but SOURCE_INDEX.json does not exist yet")

print(f"validated {len(skills)} plugin skill paths")

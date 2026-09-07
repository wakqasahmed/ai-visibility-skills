#!/usr/bin/env python3
"""Live model evaluation harness for paywall-access-audit."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contract import validate_decline_contract, validate_report_contract

EVAL_DIR = Path(__file__).resolve().parent
SKILL_DIR = EVAL_DIR.parent.parent.parent / "skills" / "ai-visibility" / EVAL_DIR.name
FIXTURES_DIR = EVAL_DIR / "fixtures"

DEFAULT_MODEL = "claude-sonnet-4-5"
DEFAULT_TRIALS = 4
DEFAULT_THRESHOLD = 0.8

DISABLED_SYSTEM_PROMPT = (
    "You are a general-purpose assistant. Respond helpfully to the user's message."
)


def build_enabled_system_prompt() -> str:
    skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    checks_file = SKILL_DIR / "references" / "checks.md"
    checks_content = (
        f"\n\n--- references/checks.md ---\n{checks_file.read_text(encoding='utf-8')}"
        if checks_file.exists()
        else ""
    )
    return (
        "You must follow this agent skill exactly as written when it applies to the "
        "user's message. If the user's message is not something this skill applies "
        "to, say so plainly instead of forcing the skill's output shape.\n\n"
        f"--- SKILL.md ---\n{skill_md}{checks_content}"
    )


def evaluate_response(fixture_name: str, response_text: str) -> dict:
    meta_file = FIXTURES_DIR / fixture_name / "meta.json"
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"passed": False, "failures": [f"invalid meta.json: {exc}"]}
    if meta.get("type", "should_use") == "should_use":
        res = validate_report_contract(response_text)
    else:
        res = validate_decline_contract(response_text)
    return {"passed": res.passed, "failures": res.failures}


def load_fixtures() -> list[dict]:
    fixtures = []
    for fixture_dir in sorted(FIXTURES_DIR.iterdir()):
        if not fixture_dir.is_dir():
            continue
        meta_file = fixture_dir / "meta.json"
        input_file = fixture_dir / "input.md"
        if not meta_file.exists() or not input_file.exists():
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        meta["_name"] = fixture_dir.name
        meta["input"] = input_file.read_text(encoding="utf-8")
        fixtures.append(meta)
    return fixtures


def call_model(client, model: str, system_prompt: str, user_message: str) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def run_condition(client, model: str, fixtures: list[dict], trials: int, enabled: bool) -> dict:
    system_prompt = build_enabled_system_prompt() if enabled else DISABLED_SYSTEM_PROMPT
    per_fixture = {}

    for meta in fixtures:
        trial_results = []
        for _ in range(trials):
            response_text = call_model(client, model, system_prompt, meta["input"])
            eval_res = evaluate_response(meta["_name"], response_text)
            trial_results.append(eval_res)
        pass_rate = mean(1.0 if t["passed"] else 0.0 for t in trial_results) if trial_results else 0.0
        per_fixture[meta["_name"]] = {
            "type": meta.get("type", "should_use"),
            "pass_rate": pass_rate,
            "trials": trial_results,
        }

    overall_pass_rate = mean(v["pass_rate"] for v in per_fixture.values()) if per_fixture else 0.0
    return {"per_fixture": per_fixture, "overall_pass_rate": overall_pass_rate}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=None, help="write JSON results here")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "SKIP: ANTHROPIC_API_KEY not set — model-harness layer no-ops. "
            "This is expected on PRs and unauthenticated runs; see README.md to run it "
            "locally or via the gated scheduled workflow."
        )
        return 0

    try:
        import anthropic
    except ImportError:
        print(
            "SKIP: ANTHROPIC_API_KEY is set but the 'anthropic' package is not installed. "
            "Run: pip install anthropic"
        )
        return 0

    client = anthropic.Anthropic(api_key=api_key)
    fixtures = load_fixtures()

    print(f"Running {args.trials} trial(s) per fixture x {len(fixtures)} fixtures x 2 conditions "
          f"(skill-enabled, skill-disabled) against {args.model}...\n")

    enabled_results = run_condition(client, args.model, fixtures, args.trials, enabled=True)
    disabled_results = run_condition(client, args.model, fixtures, args.trials, enabled=False)

    print(f"Skill-ENABLED overall pass rate:  {enabled_results['overall_pass_rate']:.2f}")
    print(f"Skill-DISABLED overall pass rate: {disabled_results['overall_pass_rate']:.2f}")
    print(f"Delta: {enabled_results['overall_pass_rate'] - disabled_results['overall_pass_rate']:+.2f}\n")

    for fixture_name, enabled_fixture in enabled_results["per_fixture"].items():
        disabled_fixture = disabled_results["per_fixture"][fixture_name]
        print(
            f"  {fixture_name}: enabled={enabled_fixture['pass_rate']:.2f} "
            f"disabled={disabled_fixture['pass_rate']:.2f}"
        )

    output = {
        "model": args.model,
        "trials": args.trials,
        "threshold": args.threshold,
        "enabled": enabled_results,
        "disabled": disabled_results,
    }
    if args.output:
        args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")
        print(f"\nWrote results to {args.output}")

    if enabled_results["overall_pass_rate"] < args.threshold:
        print(
            f"\nFAIL: skill-enabled pass rate {enabled_results['overall_pass_rate']:.2f} "
            f"is below threshold {args.threshold}"
        )
        return 1

    print(f"\nPASS: skill-enabled pass rate {enabled_results['overall_pass_rate']:.2f} "
          f">= threshold {args.threshold}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

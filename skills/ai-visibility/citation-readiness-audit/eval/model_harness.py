#!/usr/bin/env python3
"""Gated, credentialed model-harness layer for citation-readiness-audit.

Runs the real skill-enabled vs. skill-disabled ablation against a live Claude
model, using the anthropic Python SDK. This is the only layer in this eval
directory that actually invokes an LLM; it requires ANTHROPIC_API_KEY.

No-ops gracefully (prints a message, exits 0) if ANTHROPIC_API_KEY is not set,
so it is safe to reference from a scheduled/workflow_dispatch CI job without
ever failing a run for lack of credentials. See README.md for how a human
runs and verifies this.

Each fixture is fed to the model in a clean, single-turn request containing
only the fixture's input.md content plus (skill-enabled condition) the
skill's own SKILL.md and references/checks.md text — no other context,
chat history, tools, or network access. The same contract.py validator used
by run_eval.py scores the model's response, so both layers agree on what
"correct" means.

Usage:
    ANTHROPIC_API_KEY=sk-ant-... python3 model_harness.py \\
        [--trials 4] [--threshold 0.8] [--model claude-sonnet-4-5]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract  # noqa: E402

EVAL_DIR = Path(__file__).resolve().parent
SKILL_DIR = EVAL_DIR.parent
FIXTURES_DIR = EVAL_DIR / "fixtures"

DEFAULT_MODEL = "claude-sonnet-4-5"
DEFAULT_TRIALS = 4
DEFAULT_THRESHOLD = 0.8

DISABLED_SYSTEM_PROMPT = (
    "You are a general-purpose assistant. Respond helpfully to the user's message."
)


def build_enabled_system_prompt() -> str:
    skill_md = (SKILL_DIR / "SKILL.md").read_text()
    checks_md = (SKILL_DIR / "references" / "checks.md").read_text()
    return (
        "You must follow this agent skill exactly as written when it applies to the "
        "user's message. If the user's message is not something this skill applies "
        "to (no public claims to audit, wrong domain, a request to guarantee an AI "
        "outcome, a request to fabricate content, a request to expose private paths, "
        "or a direct implementation/rewrite request instead of an audit), say so "
        "plainly instead of forcing the skill's output shape.\n\n"
        f"--- SKILL.md ---\n{skill_md}\n\n"
        f"--- references/checks.md ---\n{checks_md}"
    )


def load_fixtures() -> list:
    fixtures = []
    for fixture_dir in sorted(FIXTURES_DIR.iterdir()):
        if not fixture_dir.is_dir():
            continue
        meta = json.loads((fixture_dir / "meta.json").read_text())
        meta["_dir"] = fixture_dir
        meta["input"] = (fixture_dir / "input.md").read_text()
        fixtures.append(meta)
    return fixtures


def score_response(meta: dict, response_text: str) -> list:
    if meta["category"] == "should_use":
        result = contract.check_audit_contract(
            response_text,
            expected_claim_count=meta.get("expected_claim_count"),
            expected_blocked_or_flagged_titles=meta.get("expected_blocked_or_flagged_titles") or [],
            expected_sensitive_titles=meta.get("expected_sensitive_titles") or [],
        )
        return result.failures
    else:
        result = contract.check_decline_response(
            response_text, meta.get("decline_signal_patterns") or []
        )
        return result.failures


def call_model(client, model: str, system_prompt: str, user_message: str) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def run_condition(client, model: str, fixtures: list, trials: int, enabled: bool) -> dict:
    system_prompt = build_enabled_system_prompt() if enabled else DISABLED_SYSTEM_PROMPT
    per_fixture = {}

    for meta in fixtures:
        trial_results = []
        for _ in range(trials):
            response_text = call_model(client, model, system_prompt, meta["input"])
            failures = score_response(meta, response_text)
            trial_results.append({"passed": not failures, "failures": failures})
        pass_rate = mean(1.0 if t["passed"] else 0.0 for t in trial_results)
        per_fixture[meta["_dir"].name] = {
            "category": meta["category"],
            "pass_rate": pass_rate,
            "trials": trial_results,
        }

    overall_pass_rate = mean(v["pass_rate"] for v in per_fixture.values())
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
        args.output.write_text(json.dumps(output, indent=2))
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

# Bench prompts

One folder per skill in [`skills/ai-visibility/`](../skills/ai-visibility/), each containing real, evidence-backed benchmark material for that skill — a prompt, real input evidence pulled from an actual audit, and the correct expected output for each input. Meant for use with [`wakqasahmed/skill-model-bench`](https://github.com/wakqasahmed/skill-model-bench) or any other model-comparison tool: run the same prompt across several models and score each one's output against the "correct output" shown here.

## Only real evidence, never fabricated

Every populated `bench/<skill-name>/prompt.md` traces to an audit that was actually run against a real site — the input evidence is real command output (`curl`, header dumps, response bodies), not invented. A skill with no real audit behind it yet has a `TODO.md` instead of a prompt file, stating plainly that no real benchmark material exists for it. Never a placeholder pretending to be real evidence — that would defeat the entire point of using this material as ground truth.

## Compatibility note

These files are documentation/authoring artifacts, not something `skill-model-bench`'s config generator ingests directly today — its fixture format is the structured `eval/fixtures/held-out-scenarios.json` shape (`id`/`scenario`/`expected`/`violates_gate`), not this free-form prose. To actually run one of these against `skill-model-bench`, feed the prompt and inputs to it manually (or via whatever tool you're comparing models with) until/unless a raw-prompt-file ingestion mode is added there.

# Semantic Entity & Topical Map Audit Eval Suite

This evaluation suite tests whether agents invoke `semantic-entity-topical-map-audit` on entity
disambiguation, `sameAs` knowledge-graph grounding, canonical `@id` reconciliation, and
pillar-cluster interlinking work, and decline out-of-scope tasks.

## Fixtures

- 5 positive fixtures (`should_use_01` to `05`)
- 5 boundary/negative fixtures (`should_not_use_01` to `05`)

Each fixture's `input.md` is the scenario-specific user prompt the model receives; `meta.json`
carries the fixture `type` plus a `focus` (positive) or `reason` (negative).

## What the deterministic contract enforces

`contract.py` checks the five report sections declared in the skill's Output Format, the absence of
outcome-guarantee language, entity-specific evidence markers (`sameAs`, `wikidata`, `@id`,
`jobTitle`, JSON-LD), inline command or code evidence, and — the skill's headline deliverable —
exactly one `Entity clarity classification: **VALUE**` line whose value is one of `AMBIGUOUS`,
`PARTIALLY_GROUNDED`, `FULLY_RECONCILED`. Decline responses must state a boundary *and* must not
emit the audit report's section structure.

## Running the Eval

```bash
python3 eval/ai-visibility/semantic-entity-topical-map-audit/run_eval.py
```

The live model layer (`model_harness.py`) exposes `get_system_prompt()` and
`evaluate_response(fixture_name, response_text)`, matching the other suites in this pack, and is
driven by `.github/workflows/semantic-entity-topical-map-audit-model-eval.yml`.

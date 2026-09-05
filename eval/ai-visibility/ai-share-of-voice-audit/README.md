# AI Share of Voice Audit Eval Suite

This evaluation suite tests whether agents invoke `ai-share-of-voice-audit` on operator-supplied
answer-engine transcripts, compute a cohort-scoped share of voice whose percentages reconcile with
the mention counts printed beside them, label each figure `[Measured]` or `[Derived]`, and decline
work that belongs to a sibling skill.

## Fixtures

- 6 positive fixtures (`should_use_01` to `06`)
- 6 boundary/negative fixtures (`should_not_use_01` to `06`), each probing a declared delegation or
  guardrail boundary rather than an out-of-domain refusal
- 1 ambiguous fixture (`should_clarify_01`) that requests an audit without saying whether answer
  transcripts are available

The final positive, negative, and ambiguous fixtures exercise the frontmatter trigger boundary:
select the skill for supplied-transcript analysis, do not select it for live answer collection, and
ask for transcripts when their availability is unclear.

## Layers

- **Deterministic** (`run_eval.py`, run in CI): validates the checked-in golden files against
  `contract.py` — required sections, provenance markers, a stated capture date, and numeric
  coherence of every `brand / total = pct%` figure. A green run proves the fixtures are
  well-formed, not that a model behaves.
- **Model-graded** (`model_harness.py`, run by
  `.github/workflows/ai-share-of-voice-audit-model-eval.yml` when `ANTHROPIC_API_KEY` is
  configured): feeds each fixture's `input.md` to a live model twice (skill-enabled vs.
  skill-disabled) over multiple trials, and grades every response with the same `contract.py`
  functions Layer 1 uses — `validate_report_contract` for `should_use`, `validate_decline_contract`
  for `should_not_use` and `should_clarify`. Reports the skill-enabled vs. skill-disabled pass-rate
  delta; exits `0` (`PASS`) when the skill-enabled pass rate meets `--threshold`, exits `0`
  (`SKIP`) with no model call when `ANTHROPIC_API_KEY` is unset.

## Running the Eval

```bash
python3 eval/ai-visibility/ai-share-of-voice-audit/run_eval.py
```

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 eval/ai-visibility/ai-share-of-voice-audit/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/ai-share-of-voice-audit-eval-results.json
```

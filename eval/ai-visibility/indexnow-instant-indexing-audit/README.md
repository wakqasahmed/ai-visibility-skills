# IndexNow Instant Indexing Audit Eval Suite

This evaluation suite tests whether agents invoke `indexnow-instant-indexing-audit` on IndexNow key
hosting, submission payload and `keyLocation` path scoping, and CMS push-trigger questions, and
decline out-of-scope tasks.

## Fixtures

- 6 positive fixtures (`should_use_01` to `06`)
- 5 boundary/negative fixtures (`should_not_use_01` to `05`)
- 6 held-out contract negatives (`contract_negatives/reject_01` to `06`) that the contract must
  *reject*, so the validator's failure branches are exercised rather than assumed

## Running the Eval

`run_eval.py` is deterministic: it validates the golden fixtures against the contract and asserts the
contract rejects every held-out negative.

```bash
python3 eval/ai-visibility/indexnow-instant-indexing-audit/run_eval.py
```

`model_harness.py` exposes `evaluate_response(fixture_name, response_text)` for the live model-graded
layer, driven by `.github/workflows/indexnow-instant-indexing-audit-model-eval.yml`. That layer runs
only when the `ANTHROPIC_API_KEY` secret is configured.

# answer-engine-content-audit eval

Outcome-based evaluation for the `answer-engine-content-audit` skill (issue #24).
Two layers, kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/answer-engine-content-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`answer-engine-content-audit` finds content gaps that block AI answer engines
from explaining, comparing, recommending, or supporting a product. A correct
run produces a report where:

1. There is exactly one `## Finding: ` heading per gap (independently countable
   and verifiable).
2. Every finding names the `URL` checked, the `Question` it was meant to
   answer, the `Command` run against that URL (a real `curl`/`grep` content
   pull from `references/checks.md` — not an assertion with no verification
   step), the `Observed` excerpt, a `Status`, and a `Severity`.
3. `Status` is one of `missing`, `vague`, `unciteable` — this report exists to
   surface gaps, so every finding is, by definition, not fully serving the
   question yet.
4. `Severity` is one of `critical`, `important`, `optional`, matching the
   priority vocabulary used elsewhere in this skill pack.
5. A finding marked `missing`/`unciteable` must show real absence evidence in
   `Observed` (a zero count, "no output", "no mention", etc.) — not a
   fabricated substantive excerpt for a page that was never actually pulled.
   This is `references/guardrails.md`'s "No fabrication" rule and
   `references/checks.md`'s "Evidence discipline" rule made machine-checkable.
6. A finding marked `vague` must show a real (weak) excerpt in `Observed`,
   proving the answer actually exists and was read, not just declared vague.

For inputs this skill should **not** turn into a fabricated content-gap
report (no target site given, a request to draft content directly, a page
that already passes every check, a wrong-domain request, a request to guess
findings without checking real content), correct behavior is a short
decline/defer response that does **not** contain `## Finding: ` headings.

`contract.py` implements all of the above as `check_report_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (audit requests this skill should turn into finding(s)):

| Fixture | Notable property |
|---|---|
| `should_use_01_client_side_pricing` | pricing renders client-side only — raw HTML has zero pricing text; single critical `missing` finding |
| `should_use_02_no_question_headings` | support content exists but no heading is phrased as the actual user question — `unciteable`, not missing |
| `should_use_03_missing_comparison_and_stale` | two findings on one page (no comparison language; no freshness signal) — must produce two independent findings, not one bundled finding |
| `should_use_04_vague_faq_answers` | FAQ answers exist and render server-side but are one-word stubs — `vague`, tests that `Observed` carries a real weak excerpt rather than an absence pattern |
| `should_use_05_missing_support_docs` | two separate pages/questions (data export docs missing; refund policy vague) — must tie findings to their own URLs |

**Should-not-use / near-miss** (should be declined or deferred, not forced into a fabricated report):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_no_target_site` | no site, domain, or URL given at all — nothing to fetch |
| `should_not_use_02_write_content_directly` | asks for a full ghostwritten blog post, not an audit of existing pages |
| `should_not_use_03_clean_audit` | page already passes every check.md signal — nothing to report |
| `should_not_use_04_wrong_domain_seo` | asks for traditional SEO metrics (backlinks, keyword rank, Core Web Vitals) — wrong tool entirely |
| `should_not_use_05_skip_verification_guess` | explicitly asks to skip fetching pages and guess findings by pattern-matching to "most SaaS sites" — must decline to fabricate |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill, including any raw
  `curl`/rendered-text pulls a prior step already ran.
- `meta.json` — category (`should_use` / `should_not_use`) and the specific
  assertions this fixture is meant to exercise.
- `golden_report.md` (should-use) or `golden_response.md` (should-not-use) —
  the hand-authored output a correctly-behaving agent following `SKILL.md`
  and `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
audit traces available in this repo to draw from; if any turn up later, add
them as additional fixtures rather than replacing the synthetic set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output
and asserts it satisfies `contract.py`'s rules, and that the fixture set has
at least 5 should-use and 5 should-not-use cases.

```bash
python3 skills/ai-visibility/answer-engine-content-audit/eval/run_eval.py
```

Exits `0` with `PASS: ...` when every fixture's golden output satisfies the
contract, `1` with `FAIL:` and the specific violations otherwise.

This layer proves the fixtures and the contract checks are internally
consistent and catches regressions in `contract.py` itself (a golden fixture
suddenly failing means the contract logic changed, not that a model changed
its behavior). It does **not** prove a live model given `SKILL.md` will
actually produce this exact output for a given input — that is what Layer 2
answers.

## Layer 2 — live model-harness ablation (`model_harness.py`)

Requires `ANTHROPIC_API_KEY`. Runs each fixture's `input.md` against a real
Claude model twice: once with `SKILL.md` + `references/checks.md` injected as
system instructions ("skill-enabled"), once as a bare general-purpose
assistant ("skill-disabled", no skill context at all). Scores every response
with the *same* `contract.py` functions Layer 1 uses, over multiple trials
per fixture (nondeterministic — an LLM is in the loop), and reports the
skill-enabled vs. skill-disabled pass-rate delta.

Each call is a single-turn request containing only that fixture's `input.md`
text (plus the skill text, in the enabled condition) — no prior chat
history, no tools, no other files, no network access beyond the Anthropic
API call itself. This is the "clean, disposable workspace" the scenario
requires: nothing is available to the model except what the fixture
declares.

### Running it locally (human-run verification)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 skills/ai-visibility/answer-engine-content-audit/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/answer-engine-content-audit-eval-results.json
```

- `--trials` (default 4): repetitions per fixture per condition, since a live
  model is nondeterministic. Keep in the 3-6 range per the eval's acceptance
  criteria.
- `--threshold` (default 0.8): minimum skill-enabled overall pass rate to
  exit 0. The script never fails on the skill-disabled condition — that
  condition exists only to report the delta, not to gate.
- Exits `0` and prints `PASS: ...` when the skill-enabled pass rate meets the
  threshold, `1` and `FAIL: ...` otherwise. Without `ANTHROPIC_API_KEY` set,
  it prints `SKIP: ...` and exits `0` — it never fails a run for lack of
  credentials.

Compare the printed skill-enabled vs. skill-disabled pass rates and the
per-fixture breakdown: if skill-disabled scores nearly as well as
skill-enabled, the skill isn't adding measurable value and should be
reconsidered before further investment. If skill-enabled scores well below
threshold, treat that as a signal to revise `SKILL.md`/`references/checks.md`,
not the fixtures.

### Running it in CI

`.github/workflows/answer-engine-content-audit-model-eval.yml` runs this
layer on `workflow_dispatch` and a weekly `schedule` only — never on every
PR, since it needs a paid model call. The job checks whether the
`ANTHROPIC_API_KEY` secret is configured before attempting anything live; if
it isn't, the step prints the same `SKIP: ...` message and the job succeeds
without spending any credentials or accessing the network. A repo maintainer
with access to add repository secrets must set `ANTHROPIC_API_KEY` for this
layer to actually exercise the model; until then it is a documented no-op,
not a silent gap — see the job's summary output.

## Extending it

To add a new fixture:

1. Add `fixtures/<should_use|should_not_use>_NN_<slug>/input.md`.
2. Add `meta.json` with `category`, `description`, and either
   `expected_finding_count` (should_use) or `decline_signal_patterns`
   (should_not_use).
3. Add `golden_report.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_eval.py`.

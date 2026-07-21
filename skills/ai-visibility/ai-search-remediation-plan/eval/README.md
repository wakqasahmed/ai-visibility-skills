# ai-search-remediation-plan eval

Outcome-based evaluation for the `ai-search-remediation-plan` skill (issue #22).
Two layers, kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/remediation-plan-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`ai-search-remediation-plan` converts audit findings from sibling skills into
tickets. A correct run produces a remediation plan where:

1. There is exactly one `## ` heading per ticket (independently countable and
   verifiable — `references/checks.md`'s `grep -c '^## '` check).
2. Each ticket carries either a re-runnable verification command (a fenced
   code block) or an explicit `Blocked on:` note — never neither.
3. Any ticket whose text mentions blocker language (`credential`, `access`,
   `legal`, `policy owner`, `cms access`, `approval`) is marked `Blocked on:`,
   not silently given a verification command instead — the blocker must not
   be dropped.
4. No ticket bundles more than one fix domain (e.g. a crawler fix and a schema
   fix and a content rewrite jammed into one ticket).

For inputs this skill should **not** turn into a fabricated plan (no findings,
wrong-domain request, vague non-finding ask, already-ticketed work, a direct
implementation request), correct behavior is a short decline/defer response
that does **not** contain `## ` ticket headings.

`contract.py` implements all of the above as `check_plan_contract`,
`check_blocked_tickets_present`, and `check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (audit findings this skill should turn into ticket(s)):

| Fixture | Source audit | Notable property |
|---|---|---|
| `should_use_01_robots_block` | robots-ai-crawler-audit | single critical finding, clean verification command |
| `should_use_02_missing_schema` | schema-markup-audit | single important finding, clean verification command |
| `should_use_03_sitemap_and_llms` | sitemap-discovery-audit + llms-txt-generator | two findings → must produce two independent tickets, not one bundled ticket |
| `should_use_04_thin_faq_content` | answer-engine-content-audit | optional-severity content-quality finding |
| `should_use_05_blocked_pricing_copy` | citation-readiness-audit + robots-ai-crawler-audit | one finding needs legal/CMS sign-off — must be marked `Blocked on:`, not dropped, while the other finding still gets a normal verification command |

**Should-not-use / near-miss** (should be declined or deferred, not forced into a fabricated plan):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_clean_audit` | audit came back with zero findings — nothing to convert |
| `should_not_use_02_wrong_domain_email` | request is an email marketing campaign brief, not an AI-visibility audit finding — wrong skill entirely |
| `should_not_use_03_vague_strategic_ask` | no concrete finding, just "make me more visible to AI" — nothing actionable yet |
| `should_not_use_04_already_ticketed` | input is already a well-formed, in-progress ticket — re-ticketing it would duplicate work |
| `should_not_use_05_direct_implementation_request` | ask is to directly implement/deploy a fix, not to produce a plan |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`) and the specific
  assertions this fixture is meant to exercise.
- `golden_plan.md` (should-use) or `golden_response.md` (should-not-use) — the
  hand-authored output a correctly-behaving agent following `SKILL.md` and
  `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
audit traces available in this repo to draw from; if any turn up later, add
them as additional fixtures rather than replacing the synthetic set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output
and asserts it satisfies `contract.py`'s rules, and that the fixture set has
at least 5 should-use and 5 should-not-use cases.

```bash
python3 skills/ai-visibility/ai-search-remediation-plan/eval/run_eval.py
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

Each call is a single-turn request containing only that fixture's
`input.md` text (plus the skill text, in the enabled condition) — no prior
chat history, no tools, no other files, no network access beyond the
Anthropic API call itself. This is the "clean, disposable workspace" the
scenario requires: nothing is available to the model except what the fixture
declares.

### Running it locally (human-run verification)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 skills/ai-visibility/ai-search-remediation-plan/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/remediation-plan-eval-results.json
```

- `--trials` (default 4): repetitions per fixture per condition, since a live
  model is nondeterministic. Keep in the 3-6 range per the eval's
  acceptance criteria.
- `--threshold` (default 0.8): minimum skill-enabled overall pass rate to
  exit 0. The script never fails on the skill-disabled condition — that
  condition exists only to report the delta, not to gate.
- Exits `0` and prints `PASS: ...` when the skill-enabled pass rate meets
  the threshold, `1` and `FAIL: ...` otherwise. Without `ANTHROPIC_API_KEY`
  set, it prints `SKIP: ...` and exits `0` — it never fails a run for lack
  of credentials.

Compare the printed skill-enabled vs. skill-disabled pass rates and the
per-fixture breakdown: if skill-disabled scores nearly as well as
skill-enabled, the skill isn't adding measurable value and should be
reconsidered before further investment. If skill-enabled scores well below
threshold, treat that as a signal to revise `SKILL.md`/`references/checks.md`,
not the fixtures.

### Running it in CI

`.github/workflows/remediation-plan-model-eval.yml` runs this layer on
`workflow_dispatch` and a weekly `schedule` only — never on every PR, since it
needs a paid model call. The job checks whether the `ANTHROPIC_API_KEY`
secret is configured before attempting anything live; if it isn't, the step
prints the same `SKIP: ...` message and the job succeeds without spending
any credentials or accessing the network. A repo maintainer with access to
add repository secrets must set `ANTHROPIC_API_KEY` for this layer to
actually exercise the model; until then it is a documented no-op, not a
silent gap — see the job's summary output.

## Extending it

To add a new fixture:

1. Add `fixtures/<should_use|should_not_use>_NN_<slug>/input.md`.
2. Add `meta.json` with `category`, `description`, and either
   `expected_ticket_count` / `expected_blocked_ticket_titles` (should_use) or
   `decline_signal_patterns` (should_not_use).
3. Add `golden_plan.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_eval.py`.

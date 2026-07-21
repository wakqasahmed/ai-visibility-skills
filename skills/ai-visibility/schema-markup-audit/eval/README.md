# schema-markup-audit eval

Outcome-based evaluation for the `schema-markup-audit` skill (issue #25).
Two layers, kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/schema-markup-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`schema-markup-audit` reviews a page's structured data and produces an audit
report. A correct run produces a report where:

1. All five sections from `SKILL.md`'s Output list are present: "Existing
   schema types found", "Missing or weak schema", "Mismatches with visible
   content", "Recommended JSON-LD changes", "Verification tools or
   commands".
2. "Recommended JSON-LD changes" contains a fenced ` ```json ` block that
   parses as valid JSON-LD.
3. Every property used in that JSON-LD is on the relevant page type's
   checklist from `references/checks.md` (or a generic baseline) — an
   invented/decorative property fails, per the "prefer schema that clarifies
   real entities over decorative markup" guardrail.
4. None of a fixture's declared unsupportable properties (e.g. a fabricated
   `aggregateRating` with no real reviews on the page) appear in the
   recommendation — per the "do not add schema claims that are not visible
   or supportable" guardrail.
5. "Verification tools or commands" carries a runnable command or a
   validator/rich-results URL, never neither.
6. "Mismatches with visible content" is non-empty whenever the fixture
   declares that a real mismatch exists between schema and visible content.

For inputs this skill should **not** turn into a fabricated audit report (no
concrete page, wrong-domain request, a request to invent unsupportable
ratings, an already-compliant page, a request to deploy rather than audit),
correct behavior is a short decline/defer response that does **not** contain
most of the audit-report sections.

`contract.py` implements all of the above as `check_audit_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (page/schema situations this skill should turn into a full audit report):

| Fixture | Page type | Notable property |
|---|---|---|
| `should_use_01_product_missing_offer_details` | Product | existing schema present but missing `priceCurrency`, `brand`, `sku`, `availability` |
| `should_use_02_article_missing_author_publisher` | Article | missing `dateModified`, `author`, `publisher` |
| `should_use_03_faq_content_mismatch` | FAQPage | schema answer text contradicts visible answer text, plus a missing Q&A pair |
| `should_use_04_local_business_generic_type` | LocalBusiness | typed generically instead of the specific truthful type (`Restaurant`), missing `geo`/hours/phone |
| `should_use_05_duplicate_organization_entities` | Organization | three inconsistent per-page `Organization` entities instead of one canonical entity, missing `sameAs`/`contactPoint` |

**Should-not-use / near-miss** (should be declined or deferred, not forced into a fabricated audit):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_clean_compliant_schema` | schema already covers every required property and matches visible content exactly — nothing to fix |
| `should_not_use_02_wrong_domain_email_copy` | request is an email marketing copywriting brief, not a schema/structured-data question — wrong skill entirely |
| `should_not_use_03_fabricate_reviews_request` | user explicitly asks to invent `AggregateRating`/`Review` numbers not backed by real reviews — must be declined, not turned into a recommendation |
| `should_not_use_04_vague_seo_ask` | no concrete page/URL/schema given, just "be more visible to AI" — nothing actionable yet |
| `should_not_use_05_direct_deploy_request` | ask is to directly deploy a fix to production, not to produce an audit — this skill reviews and recommends, it does not deploy |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`), the page type
  (for should_use), and the specific assertions this fixture is meant to
  exercise (`expect_mismatch`, `forbidden_properties`,
  `decline_signal_patterns`).
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
python3 skills/ai-visibility/schema-markup-audit/eval/run_eval.py
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
python3 skills/ai-visibility/schema-markup-audit/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/schema-markup-audit-eval-results.json
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

`.github/workflows/schema-markup-audit-model-eval.yml` runs this layer on
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
2. Add `meta.json` with `category`, `description`, and either `page_type` /
   `expect_mismatch` / `forbidden_properties` (should_use) or
   `decline_signal_patterns` (should_not_use).
3. Add `golden_report.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered (e.g. a new
   page type), extend `contract.py`'s `PAGE_TYPE_PROPERTIES` rather than
   special-casing it in `run_eval.py`.

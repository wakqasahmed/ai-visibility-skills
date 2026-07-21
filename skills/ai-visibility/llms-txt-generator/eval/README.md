# llms-txt-generator eval

Outcome-based evaluation for the `llms-txt-generator` skill (issue #26).
Two layers, kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/llms-txt-generator-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`llms-txt-generator` drafts or reviews an `llms.txt` file from a site's public
pages, docs, sitemap, products, policies, and support content. A correct
"should-use" run produces a full response where:

1. The proposed `llms.txt` (a fenced code block) starts with an H1 title and
   a short summary line, per the llmstxt.org convention encoded in
   `references/checks.md`.
2. It groups links into at least the fixture's expected number of `## `
   sections.
3. Every link is a markdown link to an `http(s)://` URL — no bare or
   relative links.
4. Every URL used in the draft comes from the fixture's verified source
   material (sitemap/crawl results), never a URL invented for the draft —
   the evidence-discipline rule in `references/checks.md`.
5. Thin, duplicate, or otherwise excluded pages never appear in the draft.
6. The full response also surfaces the other four items from `SKILL.md`'s
   Output contract: placement path, source URLs used, missing recommended
   URLs or pages, and verification steps — not just the file content.
7. If `/llms.txt` already returns 200, the response acknowledges the
   existing file before proposing a replacement — never a silent overwrite.
8. If a linked/expected page turns out missing or unpublished, that gap is
   named under "missing recommended URLs," not silently dropped.

For inputs this skill should **not** turn into a fabricated draft (no source
material at all, a robots.txt/crawler-access request, an explicit request to
invent unverified URLs, a "what pages should we even build" content-gap
question, or an already-fine file plus an unrelated ask), correct behavior
is a short decline/defer/redirect response that does **not** contain a
fenced H1+H2 llms.txt draft.

`contract.py` implements all of the above as `check_draft_structure`,
`check_no_fabricated_urls`, `check_no_excluded_urls`,
`check_output_sections_present`, `check_acknowledges_existing_file`,
`check_missing_pages_mentioned`, and `check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (requests this skill should turn into a drafted/reviewed `llms.txt`):

| Fixture | Notable property |
|---|---|
| `should_use_01_saas_docs_site` | clean first draft, no existing file, full verified sitemap |
| `should_use_02_ecommerce_multi_section` | multiple distinct sections (products, policies, support, company) |
| `should_use_03_existing_stale_llms_txt` | existing file (200) with one dead link — must acknowledge the existing file and drop the dead link for its verified replacement |
| `should_use_04_thin_pages_excluded` | sitemap includes thin tag-archive and duplicate print-view URLs that must be excluded |
| `should_use_05_missing_pages_noted` | a nav-linked page 404s and isn't in the sitemap — must be excluded from the draft but named under missing recommended pages |

**Should-not-use / near-miss** (should be declined or redirected, not forced into a fabricated draft):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_no_source_material` | no sitemap, page list, or crawl evidence at all — nothing to draft from |
| `should_not_use_02_wrong_domain_crawler_access` | request is to fix robots.txt crawler blocks — belongs to `robots-ai-crawler-audit` |
| `should_not_use_03_fabricate_unverified_urls` | explicit request to invent plausible-sounding URLs for pages that don't exist yet |
| `should_not_use_04_content_gap_selection_request` | asks which pages should even be built — belongs to `answer-engine-content-audit` |
| `should_not_use_05_already_fine_wants_unrelated` | llms.txt is already fine; the real ask (page-speed) is unrelated to this skill |

Each fixture directory has:
- `input.md` — the raw text/crawl evidence a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`) and the specific
  assertions this fixture is meant to exercise (`source_urls`,
  `excluded_urls`, `expected_min_sections`, `existing_llms_txt`,
  `missing_page_keywords`, or `decline_signal_patterns`).
- `golden_output.md` (should-use) or `golden_response.md` (should-not-use) —
  the hand-authored output a correctly-behaving agent following `SKILL.md`
  and `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
llms.txt-drafting traces available in this repo to draw from; if any turn up
later, add them as additional fixtures rather than replacing the synthetic
set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output
and asserts it satisfies `contract.py`'s rules, and that the fixture set has
at least 5 should-use and 5 should-not-use cases.

```bash
python3 skills/ai-visibility/llms-txt-generator/eval/run_eval.py
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
python3 skills/ai-visibility/llms-txt-generator/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/llms-txt-generator-eval-results.json
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

`.github/workflows/llms-txt-generator-model-eval.yml` runs this layer on
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
   `source_urls` / `excluded_urls` / `expected_min_sections` /
   `existing_llms_txt` / `missing_page_keywords` (should_use) or
   `decline_signal_patterns` (should_not_use).
3. Add `golden_output.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_eval.py`.

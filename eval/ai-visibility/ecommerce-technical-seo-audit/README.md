# ecommerce-technical-seo-audit eval

Outcome-based evaluation for the `ecommerce-technical-seo-audit` skill (issue #74). Two layers,
kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/ecommerce-technical-seo-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot silently
define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`ecommerce-technical-seo-audit` spot-checks 3-5 sampled category/product pages for four
catalog-specific problems: thin category pages, faceted-navigation duplicate URLs, orphan
pages, and mishandled discontinued products. A correct run produces a report with all seven
sections from `SKILL.md`'s Output list (Sample scope, Thin category/collection page findings,
Faceted-navigation duplicate URL findings, Orphan page findings, Discontinued-product handling
findings, Recommended fixes, Verification commands), where:

1. "Sample scope" explicitly discloses this is a sample (not the full catalog).
2. The report never claims or implies the full catalog / all products / all categories were
   checked — the core scope boundary that separates this free spot-check from the paid,
   full-catalog `verified-audit-skills` wrapper.
3. Every finding bullet in a section the fixture declares as `evidenced_sections` carries cited
   evidence — a status code or a concrete markup/attribute keyword (`canonical`, `noindex`,
   `robots.txt`, `sitemap`, `redirect`, `410`, `curl`, `href`) in inline code, never an
   unverified assertion.
4. "Recommended fixes" contains concrete, actionable content (inline code or a fenced block),
   and never recommends redirecting a discontinued product to the homepage/an unrelated page.
5. "Verification commands" contains a re-runnable `curl` (or equivalent) command.
6. The report never claims or implies a guaranteed AI platform outcome
   (`skills/ai-visibility/references/guardrails.md`'s "No outcome guarantees").
7. "Recommended fixes" never recommends exposing a private, authenticated, admin, or otherwise
   sensitive path.
8. None of a fixture's declared `forbidden_patterns` appear in the response.

For inputs this skill should **not** turn into a full audit report — a full-catalog crawl
request (a different, paid tier's job), a vague ask with nothing concrete to sample, a request
to fabricate a plausible-looking product URL, a request that violates a guardrail, or a
different skill's job (schema markup) — correct behavior is a short decline/defer response that
does **not** fabricate the seven-section report shape, does not claim the full catalog was
checked, and matches at least one expected decline signal.

`contract.py` implements all of the above as `check_audit_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (situations this skill should turn into a full spot-check report):

| Fixture | Scenario | Notable property |
|---|---|---|
| `should_use_01_thin_category_page_no_unique_content` | Two sibling category pages both have zero unique editorial text beyond their H1 | thin-content, scaled-template duplication |
| `should_use_02_faceted_nav_duplicate_url_no_canonical` | A color-filter variant of a category URL is crawlable/indexable with no canonical or noindex | faceted-navigation duplicate URL |
| `should_use_03_orphan_page_in_sitemap_not_linked` | A product URL is in the sitemap but absent from the homepage/category-page link crawl | orphan page |
| `should_use_04_discontinued_product_404_no_redirect` | A discontinued product 404s despite a clearly relevant in-stock successor existing | missed-redirect opportunity |
| `should_use_05_discontinued_product_redirected_to_homepage` | A discontinued product 301-redirects to the homepage instead of the closest relevant category | soft-404-risk redirect target |

**Should-not-use / near-miss** (should be declined or deferred, not forced into a fabricated report):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_full_catalog_crawl_request` | asks to crawl all 50,000 SKUs / 400 categories — this skill is a 3-5 page spot-check, not the paid full-catalog tier |
| `should_not_use_02_vague_ecommerce_seo_ask` | no concrete page/category/product given, just "traffic is down" — nothing actionable yet |
| `should_not_use_03_fabricate_product_url_request` | user asks to invent a plausible-looking discontinued product URL rather than supply a real one — must be declined, not fabricated |
| `should_not_use_04_expose_admin_inventory_path_request` | user asks to add an internal admin inventory path to the sitemap — violates the private/sensitive-path guardrail |
| `should_not_use_05_wrong_domain_schema_markup_request` | ask is a `Product`/`Offer` JSON-LD structured-data review — that's `schema-markup-audit`'s job, out of scope |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`), and either
  `evidenced_sections`/`forbidden_patterns` (should_use) or
  `decline_signal_patterns` (should_not_use).
- `golden_report.md` (should-use) or `golden_response.md` (should-not-use) — the
  hand-authored output a correctly-behaving agent following `SKILL.md` and
  `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
ecommerce-audit traces available in this repo to draw from; if any turn up later, add
them as additional fixtures rather than replacing the synthetic set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output and
asserts it satisfies `contract.py`'s rules, and that the fixture set has at least 5
should-use and 5 should-not-use cases.

```bash
python3 eval/ai-visibility/ecommerce-technical-seo-audit/run_eval.py
```

Exits `0` with `PASS: ...` when every fixture's golden output satisfies the
contract, `1` with `FAIL:` and the specific violations otherwise.

This layer proves the fixtures and the contract checks are internally consistent
and catches regressions in `contract.py` itself. It does **not** prove a live
model given `SKILL.md` will actually produce this exact output for a given input —
that is what Layer 2 answers.

## Layer 2 — live model-harness ablation (`model_harness.py`)

Requires `ANTHROPIC_API_KEY`. Runs each fixture's `input.md` against a real Claude
model twice: once with `SKILL.md` + `references/checks.md` + `references/guardrails.md`
injected as system instructions ("skill-enabled"), once as a bare general-purpose
assistant ("skill-disabled", no skill context at all). Scores every response with
the *same* `contract.py` functions Layer 1 uses, over multiple trials per fixture
(nondeterministic — an LLM is in the loop), and reports the skill-enabled vs.
skill-disabled pass-rate delta.

Each call is a single-turn request containing only that fixture's `input.md` text
(plus the skill text, in the enabled condition) — no prior chat history, no tools,
no other files, no network access beyond the Anthropic API call itself.

### Running it locally (human-run verification)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 eval/ai-visibility/ecommerce-technical-seo-audit/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/ecommerce-technical-seo-audit-eval-results.json
```

- `--trials` (default 4): repetitions per fixture per condition, since a live
  model is nondeterministic. Keep in the 3-6 range per the eval's acceptance
  criteria.
- `--threshold` (default 0.8): minimum skill-enabled overall pass rate to exit 0.
  The script never fails on the skill-disabled condition — that condition exists
  only to report the delta, not to gate.
- Exits `0` and prints `PASS: ...` when the skill-enabled pass rate meets the
  threshold, `1` and `FAIL: ...` otherwise. Without `ANTHROPIC_API_KEY` set, it
  prints `SKIP: ...` and exits `0` — it never fails a run for lack of credentials.

### Running it in CI

`.github/workflows/ecommerce-technical-seo-audit-model-eval.yml` runs this layer on
`workflow_dispatch` and a weekly `schedule` only — never on every PR, since it
needs a paid model call. The job checks whether the `ANTHROPIC_API_KEY` secret is
configured before attempting anything live; if it isn't, the step prints the same
`SKIP: ...` message and the job succeeds without spending any credentials or
accessing the network.

## Extending it

To add a new fixture:

1. Add `fixtures/<should_use|should_not_use>_NN_<slug>/input.md`.
2. Add `meta.json` with `category`, `description`, and either
   `evidenced_sections`/`forbidden_patterns` (should_use) or
   `decline_signal_patterns` (should_not_use).
3. Add `golden_report.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_eval.py`.

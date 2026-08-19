# image-audit eval

Outcome-based evaluation for the `image-audit` skill (issue #63). Two layers, kept
intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/image-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`image-audit` reviews whether images on key pages are discoverable, fetchable, and
understandable by AI crawlers and vision-capable agents. A correct run produces a
report with all six sections from `SKILL.md`'s Output list (Alt text coverage and
quality summary, Image sitemap coverage summary, ImageObject schema presence and
completeness, Fetchability findings, Recommended fixes, Verification commands), where:

1. Every finding bullet in a section the fixture declares as `evidenced_sections`
   carries cited evidence — a status code or a concrete markup/attribute keyword
   (`alt`, `image:loc`/`image:image`, `noscript`, `data-src`, `ImageObject`, `curl`)
   in inline code, never an unverified assertion.
2. "Recommended fixes" contains concrete, actionable content (inline code or a
   fenced block), not vague prose only.
3. "Verification commands" contains a re-runnable `curl` (or equivalent) command.
4. The report never claims or implies a guaranteed AI platform outcome
   (`skills/ai-visibility/references/guardrails.md`'s "No outcome guarantees").
5. "Recommended fixes" never recommends exposing a private, authenticated,
   account, or otherwise sensitive path.
6. None of a fixture's declared `forbidden_patterns` (e.g. an invented, unverifiable
   caption or credit) appear in the response — per the "do not write alt text
   describing something not depicted" guardrail.

For inputs this skill should **not** turn into a full audit report — a different
skill's job (WCAG blog-authoring accessibility guidance), a vague ask with nothing
concrete to check, a request to fabricate unverifiable image descriptions, a request
that violates a guardrail, or a request to deploy rather than audit — correct
behavior is a short decline/defer response that does **not** fabricate the
six-section report shape, and matches at least one expected decline signal.

`contract.py` implements all of the above as `check_audit_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (image-visibility situations this skill should turn into a full audit report):

| Fixture | Scenario | Notable property |
|---|---|---|
| `should_use_01_product_missing_alt_text` | Product page images missing `alt` entirely, alongside one correctly decorative `alt=""` | alt-text coverage gap |
| `should_use_02_lazy_load_no_noscript_fallback` | Hero image is JS-only lazy-load (`data-src`) with no `<noscript>` fallback | fetchability — invisible to non-JS crawlers |
| `should_use_03_image_sitemap_missing_product_images` | `sitemap.xml` declares `image:image` for a sibling page but not the audited product page | image sitemap coverage gap |
| `should_use_04_bare_url_image_schema_missing_metadata` | `Product.image` is a bare URL string despite visible photo-credit metadata on the page | `ImageObject` completeness |
| `should_use_05_auth_gated_hero_image` | Hero image URL returns `403` on a direct/bot fetch despite the page itself being public | fetchability — auth/CDN gate |

**Should-not-use / near-miss** (should be declined or deferred, not forced into a fabricated audit):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_wrong_domain_wcag_blog_accessibility` | WCAG blog-authoring accessibility guidance request — different repo's different skill, out of scope |
| `should_not_use_02_vague_ai_visibility_ask` | no concrete page/URL/markup given, just "our images don't show up" — nothing actionable yet |
| `should_not_use_03_fabricate_alt_text_request` | user asks to invent detailed alt text for photos never described — must be declined, not fabricated |
| `should_not_use_04_expose_private_image_directory_request` | user asks to expose a private customer-order photo directory to crawlers — violates the private/sensitive-path guardrail |
| `should_not_use_05_direct_deploy_request` | ask is to directly deploy a template fix to production, not to produce an audit — this skill reviews and recommends, it does not deploy |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`), and either
  `evidenced_sections`/`forbidden_patterns` (should_use) or
  `decline_signal_patterns` (should_not_use).
- `golden_report.md` (should-use) or `golden_response.md` (should-not-use) — the
  hand-authored output a correctly-behaving agent following `SKILL.md` and
  `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
image-audit traces available in this repo to draw from; if any turn up later, add
them as additional fixtures rather than replacing the synthetic set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output and
asserts it satisfies `contract.py`'s rules, and that the fixture set has at least 5
should-use and 5 should-not-use cases.

```bash
python3 eval/ai-visibility/image-audit/run_eval.py
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
python3 eval/ai-visibility/image-audit/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/image-audit-eval-results.json
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

`.github/workflows/image-audit-model-eval.yml` runs this layer on
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

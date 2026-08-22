# commerce-protocol-discovery eval

Outcome-based evaluation for the `commerce-protocol-discovery` skill. Two layers, kept
intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/commerce-protocol-discovery-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot silently
define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`commerce-protocol-discovery` classifies whether a site is ecommerce/marketplace and, if so,
runs four mechanical discovery probes (UCP business profile, A2A Agent Card, a protected MCP
endpoint's `401` challenge, and catalog feeds). A correct run produces a report with all five
sections from `SKILL.md`'s Output list (Site-type classification, UCP business profile, A2A
Agent Card, MCP, Catalog feeds), where:

1. Every finding bullet in a section the fixture declares as `evidenced_sections` carries cited
   evidence — a status code or a concrete endpoint/probe keyword (`.well-known`, `products.json`,
   `WWW-Authenticate`, `curl`, `robots.txt`, `sitemap`) in inline code, never an unverified
   assertion.
2. The response never uses a `ready`/`partial`/`missing`/`verified` scoring label anywhere — the
   core scope boundary that keeps this free discovery teaser from reproducing the private
   `commerce-protocol-readiness` skill's 5-state rubric.
3. The response never analyzes trust gates, agent/user identity, payment authorization, or
   checkout/order lifecycle behavior — entirely out of scope for a discovery-only skill.
4. The response never makes a remediation recommendation beyond the single mandated closing
   scope sentence: "Full commerce-protocol readiness scoring and remediation is a separate audit
   capability — this section only reports what's discoverable, not whether it's implemented
   correctly or safely." That exact sentence (near-verbatim) must be present.
5. The response never claims or implies a guaranteed AI platform outcome
   (`skills/ai-visibility/references/guardrails.md`'s "No outcome guarantees").
6. The response never references a private, authenticated, admin, or otherwise sensitive path.
7. None of a fixture's declared `forbidden_patterns` appear in the response.

For inputs this skill should **not** turn into a full discovery report — a request for scored
readiness/verdicts, a trust-gate/checkout-lifecycle analysis request, a remediation-planning
request, a different skill's job (full-catalog crawl), a request to fabricate/guess an MCP
endpoint, or a non-ecommerce site — correct behavior is a short decline/defer response that does
**not** fabricate the five-section report shape, does not leak scoring language, and matches at
least one expected decline signal.

`contract.py` implements all of the above as `check_discovery_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 11 scenarios, 5 should-use and 6 should-not-use/near-miss:

**Should-use** (situations this skill should turn into a full discovery report):

| Fixture | Scenario | Notable property |
|---|---|---|
| `should_use_01_ucp_profile_found_a2a_missing` | UCP profile found, A2A Agent Card 404, no MCP claimed, `products.json` found | classified via `Product`/`Offer` schema + add-to-cart |
| `should_use_02_products_json_feed_stale_price` | Catalog feed found, sampled item's price disagrees with the live product page | stale-feed cross-check reported as observed evidence, not a fail |
| `should_use_03_mcp_endpoint_401_challenge_present` | A claimed MCP endpoint returns a real `401` + `WWW-Authenticate` challenge | correct MCP probe target per checks.md |
| `should_use_04_all_four_probes_negative` | All four probes come back negative (404s, no feed, no MCP claimed) | plain "nothing found" report, not a scored failure |
| `should_use_05_marketplace_via_cart_signals_a2a_found` | No `Product` schema at all, but cart/checkout/add-to-cart signals classify it as ecommerce | fallback classification signals; A2A found |

**Should-not-use / near-miss** (should be declined or deferred, not forced into a fabricated report):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_scored_readiness_request` | asks for a ready/partial/missing/verified score — that's the private `commerce-protocol-readiness` skill's job |
| `should_not_use_02_trust_and_checkout_lifecycle_request` | asks for trust-gate and order-lifecycle analysis — entirely out of scope |
| `should_not_use_03_remediation_recommendation_request` | asks for specific implementation steps and prioritization — a remediation recommendation this skill must not make |
| `should_not_use_04_full_catalog_crawl_wrong_skill_request` | asks for thin-page/faceted-nav/orphan-page findings — that's `ecommerce-technical-seo-audit`'s job |
| `should_not_use_05_fabricate_endpoint_request` | asks to guess a site-root MCP manifest path when none is claimed — checks.md forbids this |
| `should_not_use_06_non_ecommerce_saas_site` | site classifies as SaaS docs, not ecommerce — the four probes don't apply and must not run |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`), and either
  `evidenced_sections`/`forbidden_patterns` (should_use) or
  `decline_signal_patterns` (should_not_use).
- `golden_report.md` (should-use) or `golden_response.md` (should-not-use) — the
  hand-authored output a correctly-behaving agent following `SKILL.md` and
  `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
commerce-protocol-discovery traces available in this repo to draw from; if any turn up later,
add them as additional fixtures rather than replacing the synthetic set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output and
asserts it satisfies `contract.py`'s rules, and that the fixture set has at least 5
should-use and 5 should-not-use cases.

```bash
python3 eval/ai-visibility/commerce-protocol-discovery/run_eval.py
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
python3 eval/ai-visibility/commerce-protocol-discovery/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/commerce-protocol-discovery-eval-results.json
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

`.github/workflows/commerce-protocol-discovery-model-eval.yml` runs this layer on
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

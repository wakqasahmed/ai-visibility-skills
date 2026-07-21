# robots-ai-crawler-audit eval

Outcome-based evaluation for the `robots-ai-crawler-audit` skill (issue #27).
Two layers, kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/robots-ai-crawler-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`robots-ai-crawler-audit` reviews whether crawler access rules help or block AI
visibility. A correct run produces a report with all five sections from
`SKILL.md`'s Output list (Current crawler policy summary, Blocked high-value
paths, AI crawler implications, Recommended robots.txt changes, Verification
commands), where:

1. Every claim of a blocked path in "Blocked high-value paths" carries cited
   evidence - an observed HTTP status code, an explicit `robots.txt`
   directive, or a header/meta-tag name - never an unverified assertion
   (`references/checks.md`'s evidence-discipline note: "Do not infer a block
   without an observed status code or explicit robots.txt rule").
2. "Recommended robots.txt changes" contains a concrete, re-runnable
   `User-agent`/`Allow`/`Disallow` directive, not vague prose only.
3. "Verification commands" contains a re-runnable `curl` (or equivalent)
   command.
4. The report never claims or implies a guaranteed AI platform outcome
   (`../../references/guardrails.md`'s "No outcome guarantees").
5. The report never recommends `Allow`-ing crawlers into a private,
   authenticated, admin, checkout, account, or otherwise sensitive path
   (`../../references/guardrails.md`'s "Protect private and sensitive paths").

For inputs this skill should **not** turn into a full audit report - a
different skill's job, a request that violates a guardrail, or a request with
no evidence to check - correct behavior is a short decline/redirect response
that does **not** fabricate the five-section report shape, and matches at
least one expected decline signal.

`contract.py` implements all of the above as `check_audit_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (crawler-access scenarios this skill should turn into a full report):

| Fixture | Scenario | Notable property |
|---|---|---|
| `should_use_01_gptbot_full_block` | `robots.txt` has an explicit `Disallow: /` stanza for GPTBot | site-wide block, visible in `robots.txt`, confirmed live |
| `should_use_02_xrobotstag_noindex_pricing` | `robots.txt` is clean, but `X-Robots-Tag: noindex` header blocks the pricing page | page-level header block invisible to `robots.txt`-only inspection |
| `should_use_03_meta_robots_noindex_docs` | `robots.txt` and headers are clean, but a `<meta name="robots" content="noindex, nofollow">` tag blocks a docs page | HTML-level block, likely a CMS template default |
| `should_use_04_edge_waf_block_claudebot` | `robots.txt` has no explicit ClaudeBot rule, but a live fetch as ClaudeBot returns 403 while GPTBot and a default UA return 200 | edge/WAF block invisible to `robots.txt` alone |
| `should_use_05_crawl_delay_missing_ai_stanzas` | No named AI-bot stanzas, a blanket `Crawl-delay: 20` for everyone | not a block - ambiguous policy needing explicit stanzas, with cost/scraping tradeoffs called out |

**Should-not-use / near-miss** (should be declined, redirected, or deferred, not forced into a fabricated report):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_sitemap_coverage_question` | asks about sitemap coverage, not crawler access rules - belongs to `sitemap-discovery-audit` |
| `should_not_use_02_llms_txt_drafting_request` | asks to draft an `llms.txt` file - belongs to `llms-txt-generator` |
| `should_not_use_03_vague_whole_site_visibility` | whole-site triage spanning crawling/schema/sitemap/content - belongs to `ai-visibility-audit` |
| `should_not_use_04_guarantee_without_checking` | asks the skill to assert a block with no evidence, and to guarantee a citation outcome - violates evidence discipline and the no-guarantees guardrail |
| `should_not_use_05_expose_admin_paths_request` | asks to unblock `/admin`, `/account`, `/checkout` for AI crawlers - violates the private/sensitive-path guardrail |

Each fixture directory has:
- `input.md` - the raw text a human would hand the skill (a request, plus
  fetched `robots.txt`/header/meta-tag evidence where relevant).
- `meta.json` - category (`should_use` / `should_not_use`) and the specific
  assertions this fixture is meant to exercise.
- `golden_report.md` (should-use) or `golden_response.md` (should-not-use) -
  the hand-authored output a correctly-behaving agent following `SKILL.md`
  and `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
crawler-audit traces available in this repo to draw from; if any turn up
later, add them as additional fixtures rather than replacing the synthetic
set.

## Layer 1 - deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output
and asserts it satisfies `contract.py`'s rules, and that the fixture set has
at least 5 should-use and 5 should-not-use cases.

```bash
python3 skills/ai-visibility/robots-ai-crawler-audit/eval/run_eval.py
```

Exits `0` with `PASS: ...` when every fixture's golden output satisfies the
contract, `1` with `FAIL:` and the specific violations otherwise.

This layer proves the fixtures and the contract checks are internally
consistent and catches regressions in `contract.py` itself (a golden fixture
suddenly failing means the contract logic changed, not that a model changed
its behavior). It does **not** prove a live model given `SKILL.md` will
actually produce this exact output for a given input - that is what Layer 2
answers.

## Layer 2 - live model-harness ablation (`model_harness.py`)

Requires `ANTHROPIC_API_KEY`. Runs each fixture's `input.md` against a real
Claude model twice: once with `SKILL.md` + `references/checks.md` +
`../../references/guardrails.md` injected as system instructions
("skill-enabled"), once as a bare general-purpose assistant
("skill-disabled", no skill context at all). Scores every response with the
*same* `contract.py` functions Layer 1 uses, over multiple trials per fixture
(nondeterministic - an LLM is in the loop), and reports the skill-enabled vs.
skill-disabled pass-rate delta.

Each call is a single-turn request containing only that fixture's `input.md`
text (plus the skill text, in the enabled condition) - no prior chat history,
no tools, no other files, no network access beyond the Anthropic API call
itself. This is the "clean, disposable workspace" the scenario requires:
nothing is available to the model except what the fixture declares.

### Running it locally (human-run verification)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 skills/ai-visibility/robots-ai-crawler-audit/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/robots-ai-crawler-audit-eval-results.json
```

- `--trials` (default 4): repetitions per fixture per condition, since a live
  model is nondeterministic. Keep in the 3-6 range per the eval's
  acceptance criteria.
- `--threshold` (default 0.8): minimum skill-enabled overall pass rate to
  exit 0. The script never fails on the skill-disabled condition - that
  condition exists only to report the delta, not to gate.
- Exits `0` and prints `PASS: ...` when the skill-enabled pass rate meets
  the threshold, `1` and `FAIL: ...` otherwise. Without `ANTHROPIC_API_KEY`
  set, it prints `SKIP: ...` and exits `0` - it never fails a run for lack
  of credentials.

Compare the printed skill-enabled vs. skill-disabled pass rates and the
per-fixture breakdown: if skill-disabled scores nearly as well as
skill-enabled, the skill isn't adding measurable value and should be
reconsidered before further investment. If skill-enabled scores well below
threshold, treat that as a signal to revise `SKILL.md`/`references/checks.md`,
not the fixtures.

### Running it in CI

`.github/workflows/robots-ai-crawler-audit-model-eval.yml` runs this layer on
`workflow_dispatch` and a weekly `schedule` only - never on every PR, since it
needs a paid model call. The job checks whether the `ANTHROPIC_API_KEY`
secret is configured before attempting anything live; if it isn't, the step
prints the same `SKIP: ...` message and the job succeeds without spending any
credentials or accessing the network. A repo maintainer with access to add
repository secrets must set `ANTHROPIC_API_KEY` for this layer to actually
exercise the model; until then it is a documented no-op, not a silent gap -
see the job's summary output.

## Extending it

To add a new fixture:

1. Add `fixtures/<should_use|should_not_use>_NN_<slug>/input.md`.
2. Add `meta.json` with `category`, `description`, and
   `decline_signal_patterns` (should_not_use only).
3. Add `golden_report.md` or `golden_response.md` - the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_eval.py`.

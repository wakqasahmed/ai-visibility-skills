# sitemap-discovery-audit eval

Outcome-based evaluation for the `sitemap-discovery-audit` skill (issue #28).
Two layers, kept intentionally separate:

| Layer | File | Needs credentials/network | Registered in |
|---|---|---|---|
| Deterministic contract check | `run_eval.py` + `contract.py` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/sitemap-discovery-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

Both layers score outcomes with the same `contract.py` functions, so they cannot
silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`sitemap-discovery-audit` checks whether crawlers can discover a site's
important public URLs via `sitemap.xml`, canonical tags, and redirect
behavior. A correct run produces a report where:

1. All five `SKILL.md` Output sections are present: `Sitemap paths found`,
   `Coverage gaps`, `Broken or blocked URLs`, `Canonical and redirect
   issues`, `Priority fixes` (as `## ` headings).
2. The report explicitly states that sitemap presence is not proof of
   indexing — the guardrail from `SKILL.md` and `references/checks.md`'s
   "Evidence discipline" note, never silently assumed.
3. Every finding bullet under the three evidence sections cites a concrete
   URL plus either an HTTP status code or a command/evidence code span —
   never a bare, uncited claim (`references/checks.md`'s evidence-discipline
   requirement: "URL checked, command run, observed HTTP status or XML
   content").
4. Every `Priority fixes` bullet carries an explicit priority label, so
   fixes are ranked rather than dumped as an exhaustive URL count (the
   "prioritize high-value pages over exhaustive URL counts" guardrail).
5. When a fixture expects a faceted/generated-URL crawl-noise finding, the
   report actually flags it (the "flag generated or faceted URLs" guardrail).
6. A genuinely clean sitemap (full coverage, no broken URLs, no
   canonical/redirect drift) gets reported as clean — findings are never
   fabricated to look useful.

For inputs this skill should **not** turn into a full sitemap-audit report
(wrong scope — robots.txt/bot-blocking belongs to `robots-ai-crawler-audit`,
whole-site triage belongs to `ai-visibility-audit` — a direct
implementation/deploy request, or no site given at all), correct behavior is
a short decline/redirect response that does **not** contain all five report
sections.

`contract.py` implements all of the above as `check_report_contract` and
`check_decline_response`.

## Fixtures

`fixtures/` has 10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (requests this skill should turn into a full sitemap-coverage report):

| Fixture | Notable property |
|---|---|
| `should_use_01_missing_sitemap` | no `sitemap.xml` at all, no `Sitemap:` line in `robots.txt` — the most basic discovery failure |
| `should_use_02_orphaned_pages` | sitemap exists and is well-formed, but 18 published pages are orphaned from it — a coverage gap, not a missing-sitemap failure |
| `should_use_03_broken_sitemap_urls` | sitemap lists URLs that 404/500 — broken entries, distinct from coverage gaps |
| `should_use_04_canonical_redirect_mismatch` | post-migration: sitemap URLs 301-redirect to different URLs than their own stale self-referencing canonical tags claim |
| `should_use_05_faceted_noise_stale` | sitemap flooded with faceted/generated filter-combination URLs plus stale duplicate `lastmod` values — crawl-noise finding |

**Should-not-use / near-miss** (should be declined or redirected, not forced into a fabricated report):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_clean_sitemap` | sitemap is genuinely clean — full coverage, no broken URLs, no canonical/redirect issues; correct behavior is to say so, not fabricate findings |
| `should_not_use_02_wrong_domain_robots` | request is about robots.txt bot-blocking, not sitemap coverage — belongs to `robots-ai-crawler-audit` per `SKILL.md`'s scope note |
| `should_not_use_03_wrong_domain_whole_audit` | request is for whole-site AI-visibility triage across many concerns — belongs to `ai-visibility-audit` per `SKILL.md`'s scope note |
| `should_not_use_04_direct_implementation` | ask is to directly edit and deploy `sitemap.xml`, not to audit it — this skill audits and reports, it does not implement fixes |
| `should_not_use_05_no_site_given` | no site/domain given, nothing concrete to check yet |

Each fixture directory has:
- `input.md` — the raw text a human would hand the skill.
- `meta.json` — category (`should_use` / `should_not_use`) and the specific
  assertions this fixture is meant to exercise.
- `golden_report.md` (should-use) or `golden_response.md` (should-not-use) —
  the hand-authored output a correctly-behaving agent following `SKILL.md`
  and `references/checks.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
sitemap-audit traces available in this repo to draw from; if any turn up
later, add them as additional fixtures rather than replacing the synthetic
set.

## Layer 1 — deterministic contract check (`run_eval.py`)

No network, no credentials, no LLM call. Loads every fixture's golden output
and asserts it satisfies `contract.py`'s rules, and that the fixture set has
at least 5 should-use and 5 should-not-use cases.

```bash
python3 skills/ai-visibility/sitemap-discovery-audit/eval/run_eval.py
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
python3 skills/ai-visibility/sitemap-discovery-audit/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/sitemap-discovery-audit-eval-results.json
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

`.github/workflows/sitemap-discovery-audit-model-eval.yml` runs this layer on
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
   `expected_min_findings` / `expects_faceted_flag` (should_use) or
   `decline_signal_patterns` (should_not_use).
3. Add `golden_report.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_eval.py`; it picks up any new fixture directory automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_eval.py`.

# ai-visibility-audit eval

Behavioral evaluation for the `ai-visibility-audit` skill. Three layers, kept
intentionally separate:

| Layer | File(s) | Needs credentials/network | Registered in |
|---|---|---|---|
| Checks.md regression snapshot | `run_eval.py` + `fixture/` | No | `.github/workflows/ci.yml`, every PR |
| Deterministic outcome-contract check (issue #21) | `run_outcome_eval.py` + `contract.py` + `fixtures/` | No | `.github/workflows/ci.yml`, every PR |
| Live model-harness ablation (issue #21) | `model_harness.py` + `contract.py` | Yes (`ANTHROPIC_API_KEY`) | `.github/workflows/ai-visibility-audit-model-eval.yml`, `workflow_dispatch` / weekly `schedule` only |

`run_outcome_eval.py` and `model_harness.py` both import `contract.py`, so they
score outcomes the same way and cannot silently define "correct" differently.

## What "correct" means for this skill (the outcome, not "was the skill loaded")

`ai-visibility-audit` audits a site's AI-mediated discoverability, machine-readable
context, and answer quality, then produces a ranked, evidenced report. A correct
run produces a report where:

1. An `Overall: ready|partially ready|blocked` verdict line is present.
2. Every finding is a `- [CRITICAL|IMPORTANT|OPTIONAL] Title` bullet with an
   `evidence:` citation (not just a claim) and a `delegate for deep dive:` line
   naming one of the skills in `SKILL.md`'s Delegation map
   (`robots-ai-crawler-audit`, `sitemap-discovery-audit`, `schema-markup-audit`,
   `llms-txt-generator`, `answer-engine-content-audit`, `citation-readiness-audit`,
   `ai-search-remediation-plan`).
3. No inclusion/ranking/placement/featured guarantee language appears anywhere,
   per `SKILL.md`'s guardrail (shared with `references/guardrails.md`).
4. A clean site does not get fabricated findings just to look thorough — zero
   findings and an `Overall: ready` verdict is the correct output when nothing
   is actually wrong (over-triggering check).

For inputs this skill should **not** turn into an audit report (wrong-domain
request, a demand for a platform guarantee with no site given, a direct
implementation request, an already-audited unchanged site), correct behavior
is a short decline/defer response that does **not** contain `- [SEVERITY] ...`
finding bullets and still never uses guarantee language.

`contract.py` implements all of the above as `check_audit_contract` and
`check_decline_response`.

## Layer 1 — checks.md regression snapshot (`run_eval.py` + `fixture/`)

Pre-existing (issue #3). A hand-maintained Python reimplementation of the
commands in `../references/checks.md`, run against one frozen `fixture/`
snapshot (robots.txt blocking GPTBot, missing JSON-LD, thin FAQ answers) and
asserted against severity/evidence/delegation/guardrail rules. Unchanged by
this update — see the header comment in `run_eval.py` for what it does and
does not prove.

```bash
python3 skills/ai-visibility/ai-visibility-audit/eval/run_eval.py
```

## Layer 2 — deterministic outcome-contract check (`run_outcome_eval.py`)

No network, no credentials, no LLM call. Loads every fixture under
`fixtures/*/` and asserts its golden output (`golden_report.md` for `mode:
audit`, `golden_response.md` for `mode: decline`) satisfies `contract.py`'s
rules, and that the fixture set has at least 5 `should_use` and 5
`should_not_use` cases.

```bash
python3 skills/ai-visibility/ai-visibility-audit/eval/run_outcome_eval.py
```

Exits `0` with `PASS: ...` when every fixture's golden output satisfies the
contract, `1` with `FAIL:` and the specific violations otherwise.

This layer proves the fixtures and the contract checks are internally
consistent and catches regressions in `contract.py` itself. It does **not**
prove a live model given `SKILL.md` will actually produce this exact output
for a given input — that is what Layer 3 answers.

### Fixtures (`fixtures/`)

10 scenarios, 5 should-use and 5 should-not-use/near-miss:

**Should-use** (site inputs that should produce a ranked, evidenced audit report):

| Fixture | Finding | Severity | Delegate |
|---|---|---|---|
| `should_use_01_robots_block_gptbot` | robots.txt blocks GPTBot and ClaudeBot from the whole site | critical | robots-ai-crawler-audit |
| `should_use_02_missing_schema_and_meta` | Pricing page has no meta description or JSON-LD | important | schema-markup-audit |
| `should_use_03_broken_sitemap` | sitemap.xml declared in robots.txt 404s, 200+ pages undiscoverable otherwise | important | sitemap-discovery-audit |
| `should_use_04_thin_content_faq` | FAQ answers are one to two words, too thin to cite (discoverability otherwise clean) | optional | answer-engine-content-audit |
| `should_use_05_multi_issue_ecommerce` | three simultaneous findings across all three severities and three different delegates | critical/important/optional | robots-ai-crawler-audit, schema-markup-audit, citation-readiness-audit |

**Should-not-use / near-miss** (should not produce a fabricated or forced audit report):

| Fixture | Why it's a near-miss |
|---|---|
| `should_not_use_01_clean_optimized_site` | every check in the fixture passes — correct output is zero fabricated findings and `Overall: ready`, not manufactured blockers |
| `should_not_use_02_wrong_domain_email_campaign` | request is an email marketing campaign brief, not an AI-visibility audit ask — wrong skill entirely |
| `should_not_use_03_guarantee_only_request` | user demands a platform-inclusion/ranking guarantee before giving a site — guardrail forbids the guarantee, and there's nothing to audit yet |
| `should_not_use_04_direct_implementation_request` | ask is to directly implement fixes (rewrite robots.txt, add schema) with the audit explicitly skipped — implementation is out of scope |
| `should_not_use_05_already_audited_duplicate` | user already has a complete, evidenced audit report and the site is unchanged — redoing it from scratch duplicates work |

Each fixture directory has:
- `input.md` — the raw text/site snapshot a human would hand the skill.
- `meta.json` — `category` (`should_use`/`should_not_use`), `mode`
  (`audit`/`decline`), a `description`, and the specific assertions this
  fixture is meant to exercise (`expected_min_findings`,
  `expected_max_findings`, `expected_severities`, `expected_delegates` for
  `mode: audit`; `decline_signal_patterns` for `mode: decline`).
- `golden_report.md` (`mode: audit`) or `golden_response.md` (`mode:
  decline`) — the hand-authored output a correctly-behaving agent following
  `SKILL.md` would produce.

All fixtures and golden outputs are synthetic. There are no sanitized real
audit traces available in this repo to draw from; if any turn up later, add
them as additional fixtures rather than replacing the synthetic set.

## Layer 3 — live model-harness ablation (`model_harness.py`)

Requires `ANTHROPIC_API_KEY`. Runs each fixture's `input.md` against a real
Claude model twice: once with `SKILL.md` injected as system instructions
("skill-enabled"), once as a bare general-purpose assistant ("skill-disabled",
no skill context at all). Scores every response with the *same* `contract.py`
functions Layer 2 uses, over multiple trials per fixture (nondeterministic —
an LLM is in the loop), and reports the skill-enabled vs. skill-disabled
pass-rate delta.

Each call is a single-turn request containing only that fixture's `input.md`
text (plus the skill text, in the enabled condition) — no prior chat history,
no tools, no other files, no network access beyond the Anthropic API call
itself. This is the "clean, disposable workspace" the scenario requires:
nothing is available to the model except what the fixture declares.

### Running it locally (human-run verification)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 skills/ai-visibility/ai-visibility-audit/eval/model_harness.py \
  --trials 4 --threshold 0.8 --model claude-sonnet-4-5 \
  --output /tmp/ai-visibility-audit-eval-results.json
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
threshold, treat that as a signal to revise `SKILL.md`, not the fixtures.

### Running it in CI

`.github/workflows/ai-visibility-audit-model-eval.yml` runs this layer on
`workflow_dispatch` and a weekly `schedule` only — never on every PR, since it
needs a paid model call. The job checks whether the `ANTHROPIC_API_KEY`
secret is configured before attempting anything live; if it isn't, the step
prints the same `SKIP: ...` message and the job succeeds without spending any
credentials or accessing the network. A repo maintainer with access to add
repository secrets must set `ANTHROPIC_API_KEY` for this layer to actually
exercise the model; until then it is a documented no-op, not a silent gap —
see the job's summary output.

## Extending it

To add a new outcome-contract fixture:

1. Add `fixtures/<should_use|should_not_use>_NN_<slug>/input.md`.
2. Add `meta.json` with `category`, `mode` (`audit`/`decline`),
   `description`, and either `expected_min_findings` /
   `expected_max_findings` / `expected_severities` / `expected_delegates`
   (`mode: audit`) or `decline_signal_patterns` (`mode: decline`).
3. Add `golden_report.md` or `golden_response.md` — the correct output a
   compliant agent would produce.
4. Re-run `run_outcome_eval.py`; it picks up any new fixture directory
   automatically.
5. If the new fixture exercises a contract rule not yet covered, extend
   `contract.py` rather than special-casing it in `run_outcome_eval.py`.

Keep the Layer 1 `fixture/` snapshot and its `check_*` functions in sync with
`references/checks.md` separately, per its own header comment.

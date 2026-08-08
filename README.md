# AI Visibility Skills

Canonical source for AI visibility, AEO, GEO, crawler, sitemap, schema, and citation-readiness skills.

## Install

```bash
npx skills@latest add wakqasahmed/ai-visibility-skills
```

## Contents

The installable skills live in [`skills/ai-visibility/`](skills/ai-visibility/).

## Aggregate catalogue

Changes merged to this repository are automatically synchronized to [wakqasahmed/skills](https://github.com/wakqasahmed/skills). Treat this repository as the source of truth for AI visibility skills.

## Outcome-eval harness status

`ai-search-remediation-plan` ([#22](https://github.com/wakqasahmed/ai-visibility-skills/issues/22)) has a real, working outcome-eval harness — a deterministic layer that runs free on every PR, plus a gated model-harness layer (`skills/ai-visibility/ai-search-remediation-plan/eval/model_harness.py`) that calls the Anthropic API directly to measure skill-enabled vs. skill-disabled behavior. It correctly no-ops without `ANTHROPIC_API_KEY` set as a repo secret — see [#36](https://github.com/wakqasahmed/ai-visibility-skills/issues/36) for exact setup steps. One real run of this harness costs roughly $1–2 in API calls.

The other 7 skills ([#21](https://github.com/wakqasahmed/ai-visibility-skills/issues/21), [#23](https://github.com/wakqasahmed/ai-visibility-skills/issues/23)–[#28](https://github.com/wakqasahmed/ai-visibility-skills/issues/28)) don't have this yet.

### Fund the real harness runs

This repo is one of five in the same public skills portfolio going through the same outcome-eval build-out. The full portfolio-wide cost breakdown, funding links, and per-repo targets live in [`email-marketing-skills`'s README](https://github.com/wakqasahmed/email-marketing-skills#fund-the-real-harness-runs) — this repo's share of that shared $300 target is $40 (7 unbuilt skills + iteration room on the one already proven).

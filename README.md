# AI Visibility Skills

Canonical source for AI visibility, AEO, GEO, crawler, sitemap, schema, and citation-readiness skills.

**In plain terms:** you ask whether a site is visible to AI search and answer engines (ChatGPT, Perplexity, Google AI Overviews) and the matching skill runs the relevant audit — crawler access, structured data, citation readiness, content gaps — then turns findings into a prioritized remediation checklist instead of a vague "improve your SEO."

## Install

Pick whichever fits how you work. All three end up in the same place: the skill files sitting where your agent looks for them.

### 1. Everything, via npx (recommended)

```bash
npx skills@latest add wakqasahmed/ai-visibility-skills
```

This installs every skill in the pack for whichever agent you're using (Claude Code, Cursor, Codex, and 70+ others — see the [`skills` CLI](https://github.com/vercel-labs/skills)). Add `-g` to install once for every project instead of per-project, or `-a claude-code` to target one agent specifically.

### 2. Just one skill

Don't need the whole pack? Install a single skill by its name (skill names match their folder, e.g. `ai-visibility-audit`):

```bash
npx skills@latest add wakqasahmed/ai-visibility-skills --skill ai-visibility-audit
```

Or point straight at one skill's folder on GitHub:

```bash
npx skills add https://github.com/wakqasahmed/ai-visibility-skills/tree/main/skills/ai-visibility/ai-visibility-audit
```

### 3. No Node/npx available — manual zip install

1. On this repo's GitHub page: **Code → Download ZIP**.
2. Unzip it.
3. Copy whichever `skills/ai-visibility/<name>/` folder(s) you want into your agent's own skills directory (for Claude Code, that's `.claude/skills/` in your project, or `~/.claude/skills/` for a global install; other agents use their own equivalent path).

No installer, no dependency — just files your agent already knows how to read.

### 4. Git clone

Whole pack:

```bash
git clone https://github.com/wakqasahmed/ai-visibility-skills.git
cp -r ai-visibility-skills/skills/ai-visibility/* /path/to/your/agent/skills/
```

Just one skill, via sparse-checkout (skips downloading the rest of the repo):

```bash
git clone --filter=blob:none --sparse https://github.com/wakqasahmed/ai-visibility-skills.git
cd ai-visibility-skills
git sparse-checkout set skills/ai-visibility/ai-visibility-audit
```

Then copy that skill's folder into your agent's skills directory as in method 3.

## Use it — step by step

**Start with `ai-visibility-audit`** for a general "can AI find and cite this site" check, then use the specific audits below once you know which dimension needs work.

| Skill | What it covers |
|---|---|
| [`ai-search-remediation-plan`](skills/ai-visibility/ai-search-remediation-plan/SKILL.md) | Convert AI visibility, AEO, GEO, crawler, schema, sitemap, and citation audit findings into prioritized implementation tickets or a practical remediation checklist. |
| [`ai-visibility-audit`](skills/ai-visibility/ai-visibility-audit/SKILL.md) | Audit whether ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews, and other AI agents can discover, understand, cite, and recommend a website. |
| [`answer-engine-content-audit`](skills/ai-visibility/answer-engine-content-audit/SKILL.md) | Find content gaps that prevent AI answer engines from explaining, comparing, recommending, or supporting a company, product, service, or site. |
| [`citation-readiness-audit`](skills/ai-visibility/citation-readiness-audit/SKILL.md) | Audit whether a website has stable, specific, trustworthy pages that AI systems can cite for claims, pricing, policies, docs, support answers, and company identity. |
| [`llms-txt-generator`](skills/ai-visibility/llms-txt-generator/SKILL.md) | Draft or review an `llms.txt` file from a site's public pages, docs, sitemap, products, policies, and support content. |
| [`robots-ai-crawler-audit`](skills/ai-visibility/robots-ai-crawler-audit/SKILL.md) | Review robots.txt, meta robots, headers, and AI crawler rules for search and AI-agent access. |
| [`schema-markup-audit`](skills/ai-visibility/schema-markup-audit/SKILL.md) | Audit schema.org JSON-LD and structured data for AI search, answer engines, rich results, and agent understanding. |
| [`sitemap-discovery-audit`](skills/ai-visibility/sitemap-discovery-audit/SKILL.md) | Audit sitemap coverage, canonical URLs, indexable pages, redirects, and crawl discovery paths. |

## Running an audit on your own machine

[`docs/RUNNING_AN_AUDIT.md`](docs/RUNNING_AN_AUDIT.md) walks through installing this pack
and running a skill against a real site from your own terminal — including the two most
common false positives (a `200` on `llms.txt`/`sitemap.xml` that's actually a soft-block or
an SPA fallback shell, not a real file).

## Example prompts

[`docs/EXAMPLE_PROMPTS.md`](docs/EXAMPLE_PROMPTS.md) walks through illustrative prompts
for several of these skills — the prompt text, which skill(s) it invokes, and the report
shape that skill's own `SKILL.md` promises. These are usage examples, not verified test
runs; none of them have been executed against a live site and recorded here yet.

**What actually happens when `ai-visibility-audit` runs:**

1. It classifies the site (SaaS, ecommerce, docs, etc.) and runs its own discoverability and machine-readable-context checks directly, citing command output as evidence (see `references/checks.md`).
2. For anything past that first pass, it delegates by name instead of re-implementing the check: crawler rules to `robots-ai-crawler-audit`, sitemap coverage to `sitemap-discovery-audit`, structured data to `schema-markup-audit`, `llms.txt` drafting to `llms-txt-generator`, content gaps to `answer-engine-content-audit`, citation trust to `citation-readiness-audit`.
3. It ranks the combined findings into critical / important / optional blockers.
4. It hands the ranked list to `ai-search-remediation-plan`, which turns them into a prioritized ticket list or remediation checklist.

## Design principle

Each skill in this pack states **what to check and how to report evidence** for one narrow dimension of AI visibility, then names another skill by reference for anything outside that dimension — it does not reimplement that other skill's checks inline. `robots-ai-crawler-audit`'s own scope line makes this explicit: *"Sitemap coverage belongs to `sitemap-discovery-audit`; drafting `llms.txt` belongs to `llms-txt-generator`; whole-site triage belongs to `ai-visibility-audit`."* `ai-visibility-audit` runs the same pattern from the top: it does its own discoverability pass, then its "Delegation" section hands each deeper check to the specialist skill that owns it instead of duplicating that logic.

- **Bad:** a skill that, on finding a citation-readiness problem, starts parsing JSON-LD and grading schema completeness inline — that's `schema-markup-audit`'s job, and now there are two divergent implementations of the same check to keep in sync.
- **Good:** the skill says "structured data needs a deeper pass — see `schema-markup-audit`" and cites what that skill covers, staying in its own lane.

This keeps each skill small and keeps the check logic in exactly one place, so a fix to how sitemaps are audited only has to happen inside `sitemap-discovery-audit`.

## Contents

The installable skills live in [`skills/ai-visibility/`](skills/ai-visibility/).

## Aggregate catalogue

Changes merged to this repository are automatically synchronized to [wakqasahmed/skills](https://github.com/wakqasahmed/skills). Treat this repository as the source of truth for AI visibility skills.

## Outcome-eval harness status

`ai-search-remediation-plan` ([#22](https://github.com/wakqasahmed/ai-visibility-skills/issues/22)) has a real, working outcome-eval harness — a deterministic layer that runs free on every PR, plus a gated model-harness layer (`eval/ai-visibility/ai-search-remediation-plan/model_harness.py`) that calls the Anthropic API directly to measure skill-enabled vs. skill-disabled behavior. It correctly no-ops without `ANTHROPIC_API_KEY` set as a repo secret — see [#36](https://github.com/wakqasahmed/ai-visibility-skills/issues/36) for exact setup steps. One real run of this harness costs roughly $1–2 in API calls.

The other 7 skills ([#21](https://github.com/wakqasahmed/ai-visibility-skills/issues/21), [#23](https://github.com/wakqasahmed/ai-visibility-skills/issues/23)–[#28](https://github.com/wakqasahmed/ai-visibility-skills/issues/28)) don't have this yet.

### Fund the real harness runs

This skill's deterministic checks run free on every PR. Proving its outcome-eval harness with real, metered model calls costs money:

- **Bitcoin (BTC):** `bc1p5xqamscrz7nu0d8jdmj748rj75sk8khtyxypn3qvsdjms4t4uw2qsjn0he`
- **Ethereum (ETH) / any ERC-20 including stablecoins:** `0x59bc573e414D62d44461234dEf438247dfc3Cf6A`

Double-check every character against this page before sending. Full portfolio picture and rationale: [wakqasahmed/skills](https://github.com/wakqasahmed/skills#fund-the-real-harness-runs).

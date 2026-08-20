# feat(skill): add paywall-access-audit skill

**Labels:** `enhancement`, `skill`, `eval`

## Problem

Publishers, news sites, research journals, premium newsletters, and subscription platforms want their articles, papers, and premium reports to be discoverable in AI search results (Google AI Overviews, Perplexity, ChatGPT Search) and cited as authoritative sources, without allowing full paywall bypass or unauthorized full-text data scraping.

Common technical failure modes for paywalled/metered content in AI search:
1. **Missing or invalid `isAccessibleForFree` schema markup:** Without Schema.org `NewsArticle` / `CreativeWork` `isAccessibleForFree: "False"` and `hasPart` with `cssSelector` declarations, Google and AI bots treat the paywall overlay as cloaking or thin content.
2. **Cloaking false-positives:** Serving full HTML to Googlebot/AI bots while returning a hard 403 or blank body to user-facing AI tools (like `ChatGPT-User` or `Claude-User`), leading to crawler penalties or citation failures.
3. **Inconsistent crawler rules for training vs. search citation:** Misconfiguring `Google-Extended`, `Claude-SearchBot`, or `OAI-SearchBot` such that discovery/citation bots are blocked alongside training crawlers.
4. **Metered paywalls with broken client-side gating:** Rendering full premium content in client-side HTML hidden only with `display: none` or CSS blur, exposing full proprietary text to all crawlers while claiming paywalled status.

Currently, existing skills cover general crawler access and general schema, but no skill audits paywall structured data conformance or subscription access boundaries.

## Proposed Scope & Lane

`paywall-access-audit` audits whether paywalled and subscription-gated publications follow Google, Schema.org, and AI crawler conventions for paywalled content transparency.

**In-Scope:**
1. Conformance with Schema.org paywall specification (`isAccessibleForFree: false`, `hasPart` specifying CSS selectors for gated sections).
2. Lead-in / preview snippet visibility check (verifying the public lead paragraph is crawlable and matches structured metadata).
3. AI training crawler (`Google-Extended`, `Applebot-Extended`, `GPTBot`) vs. search/citation crawler (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`) policy separation for paywalled domains.
4. Detection of cloaking risks (verifying headers and status codes returned to search crawlers vs. generic agents).

**Delegation / Out-of-Scope:**
- General whole-site triage belongs to `ai-visibility-audit`.
- Whole-site `robots.txt` auditing belongs to `robots-ai-crawler-audit`.
- General structured data beyond paywall tags belongs to `schema-markup-audit`.
- Article content gap analysis belongs to `answer-engine-content-audit`.

## Citations to Register
- `GOOGLE-PAYWALL-SCHEMA-01`: Google Search Central, *Structured data for paywalled content (NewsArticle, CreativeWork isAccessibleForFree)*.
- `SCHEMA-ISACCESSIBLEFORFREE-01`: Schema.org, *isAccessibleForFree property on CreativeWork*.

## Acceptance Criteria
- [ ] Create `skills/ai-visibility/paywall-access-audit/SKILL.md` with standard frontmatter, scope, workflow, output format, and guardrails.
- [ ] Create `skills/ai-visibility/paywall-access-audit/references/checks.md` with extraction commands for `isAccessibleForFree` JSON-LD, lead-in snippet verification, and paywall bot header inspection.
- [ ] Create `skills/ai-visibility/paywall-access-audit/references/guardrails.md` (and canonical sync).
- [ ] Create `eval/ai-visibility/paywall-access-audit/` containing `contract.py`, `run_eval.py`, `model_harness.py`, `README.md`, and 10 fixtures (5 `should_use`, 5 `should_not_use`).
- [ ] Add `paywall-access-audit` to:
  - `.claude-plugin/plugin.json`
  - `manifest.json` (bump `skill_count` and `source_count`)
  - `README.md` skill table
  - `SOURCES.md` and `SOURCE_INDEX.json`
  - `docs/EXAMPLE_PROMPTS.md`
  - `bench/paywall-access-audit/TODO.md`
  - `skills/ai-visibility/ai-visibility-audit/SKILL.md` (Delegation section)
  - `skills/ai-visibility/ai-search-remediation-plan/references/checks.md`
- [ ] Add deterministic test step to `.github/workflows/ci.yml` and add `.github/workflows/paywall-access-audit-model-eval.yml`.
- [ ] All validators pass: `validate-plugin.py`, `validate-citations.py`, and `run_eval.py`.

## Risk Level
Low — additive new skill with zero breaking changes to existing skills.

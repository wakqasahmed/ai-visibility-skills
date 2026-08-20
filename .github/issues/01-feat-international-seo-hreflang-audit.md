# feat(skill): add international-seo-hreflang-audit skill

**Labels:** `enhancement`, `skill`, `eval`

## Problem

Global websites often serve multilingual or multi-regional content across different language codes, ccTLDs, subdomains, or path prefixes (e.g., `/en/`, `/es/`, `/de/`, `/fr-ca/`). AI answer engines (ChatGPT Search, Perplexity, Google AI Overviews) frequently fetch regional URLs or summarize multi-lingual content based on user locale. When `hreflang` tags, `x-default` fallbacks, canonical cross-references, and localized XML sitemaps are missing, misconfigured, or conflicting:
- AI engines index and cite the wrong regional variation (e.g., US English pricing for UK/EU queries).
- Crawler budget is wasted on duplicated regional pages without canonical/hreflang signals.
- Broken bidirectional return tags (`hreflang` on page A pointing to page B, but page B missing return link to A) cause search crawlers and AI bots to drop regional clustering.

Currently, none of the 10 skills in `ai-visibility-skills` specifically spot-checks or validates internationalization, `hreflang` implementations, or regional locale discoverability.

## Proposed Scope & Lane

`international-seo-hreflang-audit` will spot-check multi-language and multi-regional implementations for AI visibility and search indexing.

**In-Scope:**
1. Bidirectional `hreflang` verification across sampled locale pages (`<link rel="alternate" hreflang="..." href="...">` and HTTP header `Link:`).
2. Presence and validity of `x-default` fallback declaration.
3. Language and country ISO code validity (ISO 639-1 language, ISO 3166-1 Alpha-2 region format, e.g. `en-US`, `pt-BR`).
4. Canonical vs. hreflang URL alignment (each localized alternate URL must self-canonicalize or point to its own distinct URL, not canonicalize back to default).
5. Localized XML sitemap declarations (`xhtml:link` entries in `sitemap.xml`).

**Delegation / Out-of-Scope:**
- General whole-site triage belongs to `ai-visibility-audit`.
- Single-region crawler/robots rules belong to `robots-ai-crawler-audit`.
- General page sitemap checks belong to `sitemap-discovery-audit`.
- Catalog-specific ecommerce faceted duplicate checks belong to `ecommerce-technical-seo-audit`.

## Citations to Register
- `GOOGLE-HREFLANG-01`: Google Search Central, *Localized versions of your pages / Tell Google about localized versions of your page*.
- `W3C-ISO-LANG-01`: W3C / IANA Language Subtag Registry, *Language tags in HTML and XML*.

## Acceptance Criteria
- [ ] Create `skills/ai-visibility/international-seo-hreflang-audit/SKILL.md` with standard frontmatter, scope, workflow, output format, and guardrails.
- [ ] Create `skills/ai-visibility/international-seo-hreflang-audit/references/checks.md` with curl / grep commands for extracting `hreflang` tags, HTTP Link headers, checking return tags, and verifying `x-default`.
- [ ] Create `skills/ai-visibility/international-seo-hreflang-audit/references/guardrails.md` (and canonical sync).
- [ ] Create `eval/ai-visibility/international-seo-hreflang-audit/` containing `contract.py`, `run_eval.py`, `model_harness.py`, `README.md`, and 10 fixtures (5 `should_use`, 5 `should_not_use`).
- [ ] Add `international-seo-hreflang-audit` to:
  - `.claude-plugin/plugin.json`
  - `manifest.json` (bump `skill_count` and `source_count`)
  - `README.md` skill table
  - `SOURCES.md` and `SOURCE_INDEX.json`
  - `docs/EXAMPLE_PROMPTS.md`
  - `bench/international-seo-hreflang-audit/TODO.md`
  - `skills/ai-visibility/ai-visibility-audit/SKILL.md` (Delegation section)
  - `skills/ai-visibility/ai-search-remediation-plan/references/checks.md`
- [ ] Add deterministic test step to `.github/workflows/ci.yml` and add `.github/workflows/international-seo-hreflang-audit-model-eval.yml`.
- [ ] All validators pass: `validate-plugin.py`, `validate-citations.py`, and `run_eval.py`.

## Risk Level
Low — additive new skill with zero breaking changes to existing skills.

---
name: international-seo-hreflang-audit
description: Audit whether multi-region, multilingual, and localized website implementations correctly declare hreflang annotations, x-default fallbacks, language codes, and canonical relationships for AI search engines.
---

# International SEO & Hreflang Visibility Audit

Audit multilingual and multi-regional website configurations to ensure search engines and AI answer engines correctly index, disambiguate, and cite regional content (pricing, currency, inventory, and language variations).

## Workflow

1. **Discover Language & Regional Architecture**:
   - Inspect sampled URLs across language/regional prefixes (`/en/`, `/es/`, `/de/`, `/fr-ca/`), subdomains (`uk.example.com`), or ccTLDs.
   - Extract `<link rel="alternate" hreflang="..." href="...">` tags in HTML `<head>` and `Link:` HTTP response headers `[GOOGLE-HREFLANG-01]`.
   - Inspect XML sitemaps for `xhtml:link` localized alternate declarations `[GOOGLE-HREFLANG-01]`.

2. **Verify Language & Region Code Validity**:
   - Validate language subtags against ISO 639-1 (e.g., `en`, `es`, `de`, `fr`, `zh`) `[W3C-ISO-LANG-01]`.
   - Validate optional regional subtags against ISO 3166-1 Alpha-2 (e.g., `en-US`, `en-GB`, `es-MX`, `pt-BR`) `[W3C-ISO-LANG-01]`.
   - Flag invalid combinations (e.g., using country codes as language codes, or using script codes incorrectly).

3. **Audit Bidirectional Return Links (Reciprocity)**:
   - For every sampled page A with `hreflang` pointing to alternate page B, fetch page B and verify it contains a reciprocal `hreflang` link pointing back to page A `[GOOGLE-HREFLANG-01]`.
   - Flag broken or missing return links that cause search engines to ignore regional clustering.

4. **Verify `x-default` Fallback**:
   - Confirm the presence of `hreflang="x-default"` for landing pages or international selectors when a user's language/region is not explicitly targeted `[GOOGLE-HREFLANG-01]`.

5. **Cross-Check Localized Canonical Alignment**:
   - Ensure each localized alternate page has a self-referential canonical `<link rel="canonical">` pointing to its own regional URL `[GOOGLE-HREFLANG-01]`.
   - Flag localized pages that incorrectly point canonicals back to the default/global root, which causes AI engines to de-index regional pages.

6. **Classify Findings & Deliver Remediation**:
   - Report missing bidirectional links, uncanonicalized alternates, invalid ISO codes, and missing `x-default` declarations with curl reproduction commands.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Core robots.txt access and edge blocking → `robots-ai-crawler-audit`
- General XML sitemap health → `sitemap-discovery-audit`
- Developer tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Reports must contain:
1. **Target Locale Matrix**: List of sampled URLs, declared `hreflang` values, HTTP status codes, and canonical URLs.
2. **Hreflang Conformance Table**: Reciprocity status, `x-default` presence, and ISO code validity.
3. **Itemized Findings**: Detailed issue cards with Evidence Tier, severity, reproduction command, and remediation snippet.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for cross-cutting rules on outcome guarantees and factual evidence.

- Distinguish observed HTML/header annotations (`High [Measured]`) from inferred locale targeting.
- Do not flag single-language, single-region sites for lacking `hreflang` (mark check as N/A).

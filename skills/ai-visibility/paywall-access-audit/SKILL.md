---
name: paywall-access-audit
description: Audit whether paywalled, metered, and subscription-gated publications follow Schema.org paywall specifications, provide crawlable lead-in snippets, and correctly configure AI crawler access policies.
---

# Paywall & Subscription Content Access Audit

Audit subscription-gated publications, research portals, newsletters, and premium content platforms to ensure search engines and AI answer engines can discover, understand, and cite authoritative articles without triggering cloaking penalties or unauthorized full-text scraping.

## Workflow

1. **Audit Schema.org Paywall Markup Conformance**:
   - Inspect JSON-LD on sample paywalled pages for `NewsArticle`, `Article`, or `CreativeWork` entities `[GOOGLE-PAYWALL-SCHEMA-01]`.
   - Verify `isAccessibleForFree: "False"` (or boolean `false`) `[SCHEMA-ISACCESSIBLEFORFREE-01]`.
   - Verify `hasPart` contains `WebPageElement` with `isAccessibleForFree: "False"` and valid `cssSelector` matching the gated content wrapper `[GOOGLE-PAYWALL-SCHEMA-01]`.

2. **Audit Lead-In / Preview Snippet Server-Side Renderability**:
   - Verify that the public lead paragraph, headline, author, and date exist in the raw HTML payload (`curl -s "$URL"`).
   - Ensure the public lead-in is not hidden with client-side JavaScript or CSS that causes AI crawlers to perceive the page as empty or cloaked.

3. **Separate AI Training vs. AI Search/Citation Crawler Policies**:
   - Audit `robots.txt` for separation of AI training bots (`GPTBot`, `Google-Extended`, `Applebot-Extended`) versus AI search citation bots (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`).
   - Flag configurations that accidentally block citation bots, preventing paywalled research from being cited in AI search results.

4. **Audit Cloaking & Edge Status Consistency**:
   - Compare HTTP status codes and headers returned to search bots vs. standard user-agents to detect accidental cloaking or hard WAF blocks.

5. **Classify Findings & Deliver Remediation**:
   - Provide concrete fixes: Schema.org `isAccessibleForFree` JSON-LD templates, CSS selector alignments, and `robots.txt` crawler policies.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Core robots.txt access and edge blocking → `robots-ai-crawler-audit`
- General structured data beyond paywall properties → `schema-markup-audit`
- Content gap analysis on free/public pages → `answer-engine-content-audit`
- Developer tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Reports must contain:
1. **Paywall Specification Conformance Matrix**: Tested URLs, `isAccessibleForFree` status, `hasPart` selector validity.
2. **Lead-In Snippet Renderability & Visibility**: SSR verification of public lead paragraphs.
3. **AI Crawler Policy Separation**: Analysis of training vs. citation bots in `robots.txt`.
4. **Recommended Fixes**: Schema blueprints, selector alignments, and robots policy adjustments.
5. **Verification Commands**: Reproducible curl commands.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for cross-cutting rules on outcome guarantees and factual evidence.

- Distinguish observed Schema.org properties (`High [Measured]`) from inferred subscription model rules.
- Do not attempt to bypass, crack, or circumvent client-side or server-side paywalls.

---
name: robots-ai-crawler-audit
description: Review robots.txt, meta robots, headers, and AI crawler rules for search and AI-agent access. Use when a user asks why AI tools cannot find, read, or cite their site.
---

# Robots AI Crawler Audit

Check whether crawler access rules help or block AI visibility.

Scope: access rules only. Sitemap coverage belongs to `sitemap-discovery-audit`; drafting `llms.txt` belongs to `llms-txt-generator`; whole-site triage belongs to `ai-visibility-audit`.

## Workflow

1. Fetch `/robots.txt`.
2. Identify global disallow rules, sitemap declarations, crawl delays, and user-agent specific rules. On ecommerce/marketplace sites, check specifically whether product, category, and policy paths are blocked — these are usually the pages a shopper or AI agent needs to read.
3. Check page-level `noindex`, `nofollow`, canonical tags, and Google snippet preview controls on key URLs.
   - Inspect `<meta name="robots">`, the Google-specific `<meta name="googlebot">` form, and `X-Robots-Tag` for `nosnippet`, `max-snippet:N`, and `max-image-preview:{none|standard|large}`, then sweep `div`/`span`/`section` elements for `data-nosnippet` [GOOGLE-ROBOTS-META-01].
   - Treat `nosnippet` and `max-snippet:0` (via either meta name) as Google AI Overviews and AI Mode exclusions. Report positive `max-snippet` limits, `max-image-preview` limits, and `data-nosnippet` regions on `div`/`span`/`section` as scoped preview restrictions rather than full-page indexing blocks; report `data-nosnippet` on any other element as invalid markup, not an active restriction [GOOGLE-AI-FEATURES-01].
4. Check response security headers (`Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`) on key URLs — a real technical-SEO/trust signal, and missing ones can also indicate a misconfigured origin worth flagging alongside crawler-access findings.
5. Look for AI crawler-specific rules for major bots where visible.
6. Compare access rules against the user's visibility goals.
7. [EXPERIMENTAL] Check for emerging draft signals (Content Signals directives in robots.txt, Web Bot Auth endpoints/headers, and DNS-AID TXT records) — see `references/checks.md`. Clearly mark any findings in this category as experimental draft standards that do not block core search/crawler indexing.
8. Recommend exact changes only when the desired access policy is clear.

## Output

- Current crawler policy summary
- Blocked high-value paths
- AI crawler implications
- Google snippet preview restrictions (`nosnippet`, `max-snippet`, and `max-image-preview`) by key URL and delivery channel (meta tag or header)
- `data-nosnippet` regions found on each key URL
- Security header gaps (HSTS, X-Content-Type-Options, X-Frame-Options)
- [EXPERIMENTAL] Emerging protocol signals (Content Signals, Web Bot Auth, DNS-AID) — clearly labeled as optional draft standards
- Recommended robots.txt changes
- Verification commands

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on not
exposing private/sensitive paths and not claiming AI platform outcome guarantees.

- Call out tradeoffs between visibility, cost, scraping risk, and content control.

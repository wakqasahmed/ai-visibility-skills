---
name: ecommerce-technical-seo-audit
description: Spot-check an ecommerce site for the technical-SEO problems most specific to catalogs — thin category pages, faceted-navigation duplicate URLs, orphan pages, and mishandled discontinued products. Use when a user wants a quick, sample-based read on ecommerce-specific crawl/index health, not a full-catalog crawl.
---

# Ecommerce Technical SEO Audit

Sample a handful of category, collection, and product pages to check for the technical-SEO
problems that are specific to ecommerce catalogs rather than generic site-wide issues.

Scope: this is a **spot-check for free-tier credibility-building, not an exhaustive audit**.
Sample 3-5 category/product pages and report what the sample actually shows — this is not a
full-catalog crawl, and the report must never claim or imply the entire catalog was checked.
The exhaustive, full-catalog, traffic-prioritized version of these same checks (crawling every
category and product URL, cross-referenced against real GA4 traffic/conversion data) lives in a
separate private/paid pack (`verified-audit-skills`'s `04-ecommerce-verified-audit-wrapper`) —
this skill is the free teaser, not a duplicate of that paid differentiator.

Generic sitemap coverage, canonical tags, and broken-link sweeps belong to
`sitemap-discovery-audit`; crawler/robots access rules belong to `robots-ai-crawler-audit`;
structured data depth (`Product`, `Offer` schema) belongs to `schema-markup-audit`; whole-site
triage belongs to `ai-visibility-audit`. This skill only covers the four catalog-specific checks
below.

## Workflow

1. Sample 3-5 category/collection pages and 3-5 product pages — pick a mix (a top-level
   category, a narrow sub-category, a well-known product, and, if discoverable, an older/less
   prominent one). Do not attempt to crawl the full catalog.
2. Check each sampled category/collection page for thin content: word count of unique on-page
   text (excluding nav, product-grid text, and boilerplate) and whether it duplicates another
   category's copy.
3. Check for faceted-navigation duplicate URLs: apply a filter or sort option on a sampled
   category page and check whether it produces a separately crawlable/indexable URL (query
   parameters, no canonical back to the base URL, no `noindex`, not blocked in robots.txt).
4. Check for orphan pages: for each sampled URL, check whether it is reachable from on-site
   navigation (nav, category grid, internal links) as well as present in the sitemap — a page in
   the sitemap with no discoverable internal link pointing to it is an orphan.
5. Check discontinued-product handling: if an old/discontinued product URL is discoverable
   (from the sitemap, a search engine cache, or a user-supplied list), check its status code and
   whether it redirects to a relevant replacement product/category or returns a proper
   404/410 — as opposed to a generic 404 with no path forward, or a soft-404 (200 status with
   error-page content), or a redirect to an unrelated page/homepage.
6. Report findings as a sample, explicitly stating the sample size and pages checked — never as
   a catalog-wide conclusion.

Use the commands in `references/checks.md` for each check.

## Output

- Sample scope (exact pages/URLs checked, and that this is a sample, not the full catalog)
- Thin category/collection page findings (word count, duplication)
- Faceted-navigation duplicate URL findings
- Orphan page findings
- Discontinued-product handling findings
- Recommended fixes
- Verification commands

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on not
claiming AI platform outcome guarantees, not fabricating unverifiable claims, and not
exposing private/sensitive paths.

- Never state or imply that the full catalog, or "all products/categories," was checked —
  state the exact sample size and which pages were sampled every time.
- Do not extrapolate a sample finding into a catalog-wide count (e.g. do not claim "N thin
  pages site-wide" from a 3-5 page sample) — report what the sample shows and recommend a
  full-catalog crawl as the next step if the client wants exhaustive coverage.
- Do not recommend a specific word-count target as a ranking guarantee — thin-content
  thresholds are practitioner guidance, not an official Google minimum; say so.
- Do not recommend redirecting a discontinued product to an irrelevant page (homepage, an
  unrelated category) — an irrelevant-target redirect risks being treated as a soft 404.

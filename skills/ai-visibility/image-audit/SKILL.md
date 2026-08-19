---
name: image-audit
description: Audit whether images on key pages are visible to AI crawlers and vision-capable agents — alt text, image sitemap coverage, ImageObject schema, and fetchability. Use for product, category, and hero image AI-visibility reviews.
---

# Image Audit

Check whether a site's images can actually be discovered, fetched, and understood by AI crawlers and vision-capable agents.

Scope: public-signal image audit against a live site (alt text, image sitemap, `ImageObject` schema, fetchability). This is not a WCAG/accessibility authoring guide for blog content — that belongs to the blog-writing skill pack. Structured data beyond images belongs to `schema-markup-audit`; sitemap coverage for pages (not images) belongs to `sitemap-discovery-audit`.

## Workflow

1. Identify key pages to sample: product pages, category/listing pages, and any page with a hero image.
2. Check `alt` text presence and quality on each sampled page's key images.
3. Check whether `sitemap.xml` declares `<image:image>` entries for those same images.
4. Check whether `ImageObject` schema is present and complete where relevant (e.g. `Product.image` as a full `ImageObject` vs a bare URL string).
5. Check fetchability: whether the image is reachable without executing JavaScript, and whether a `<noscript>` fallback exists for JS-only lazy-loaded images; whether the image request requires authentication or returns a geo-blocked response.
6. Prioritize fixes that unblock the most images with the least effort (e.g. a missing `<noscript>` fallback template affects every lazy-loaded image site-wide).

Use the extraction and fetch commands in `references/checks.md`.

## Output

- Alt text coverage and quality summary (key pages sampled, missing/weak count)
- Image sitemap coverage summary (declared vs. found on page)
- `ImageObject` schema presence and completeness
- Fetchability findings (JS-only lazy-load without fallback, auth/geo-blocked images)
- Recommended fixes
- Verification commands

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on not
claiming AI platform outcome guarantees, not fabricating unverifiable claims, and not
exposing private/sensitive paths.

- Do not write alt text that describes something not actually depicted in the image — only flag missing/weak alt text and suggest what to verify, since the audit cannot see the image content itself.
- Treat a `<noscript>` fallback or `<img>` fallback `src` as required wherever lazy-loading is used; a JS-only image with no fallback is a finding regardless of how it renders in a browser.

## Sample scope

Sample of 1 category page and its `?color=blue` facet variant, out of an unknown total
category/facet-combination count — this is a spot-check, not a full-catalog crawl.

## Thin category/collection page findings

Not checked in this sample — no on-page text was supplied for word-count analysis.

## Faceted-navigation duplicate URL findings

- `mens-running-shoes?color=blue` returns `200`, has no `canonical` tag pointing back to the
  base `mens-running-shoes` URL, and no `noindex` meta tag — it is a crawlable, indexable
  near-duplicate of the base category page.
- `robots.txt` has no `disallow` rule for the `color=` parameter, so nothing prevents a crawler
  from reaching and indexing this and every other color-filter combination separately.
- The base `mens-running-shoes` URL does carry its own self-referencing `canonical` — the gap is
  specific to the filtered variant, not the base page.

## Orphan page findings

Not checked in this sample — no sitemap or navigation data was supplied.

## Discontinued-product handling findings

Not checked in this sample — no product URLs were supplied.

## Recommended fixes

Add a `canonical` tag on every filtered/sorted URL pointing back to the unfiltered base
category, so the facet variant stops competing with it as a separate indexable page:

```html
<link rel="canonical" href="https://shop.example.com/collections/mens-running-shoes">
```

If facet URLs should not be crawled at all, add a `disallow` rule scoped to the parameter
instead:

```
User-agent: *
Disallow: /collections/*?color=
```

## Verification commands

```bash
curl -s "https://shop.example.com/collections/mens-running-shoes?color=blue" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
curl -s "https://shop.example.com/robots.txt" | grep -iE 'disallow.*color='
```

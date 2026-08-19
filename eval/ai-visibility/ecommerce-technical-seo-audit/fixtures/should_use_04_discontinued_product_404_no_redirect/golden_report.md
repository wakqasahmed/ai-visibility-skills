## Sample scope

Sample of 1 discontinued product URL checked, out of an unknown total discontinued-product
count — this is a spot-check, not a full-catalog crawl.

## Thin category/collection page findings

Not checked in this sample — no category-page text was supplied.

## Faceted-navigation duplicate URL findings

Not checked in this sample — no filter/sort variant was supplied.

## Orphan page findings

Not checked in this sample — no sitemap or navigation data was supplied.

## Discontinued-product handling findings

- `trail-runner-boot-v1` returns a bare `404` with no redirect, even though
  `trail-runner-boot-v2` is a directly relevant, in-stock replacement (same product line,
  updated sole) — this is a missed opportunity to preserve the old URL's SEO value via a
  targeted `301` redirect rather than a dead end.
- A bare `404` would be the correct call only if no relevant replacement existed; here one
  clearly does.

## Recommended fixes

Redirect the discontinued product to its specific replacement, not a category page or the
homepage:

```
301 https://shop.example.com/products/trail-runner-boot-v1 -> https://shop.example.com/products/trail-runner-boot-v2
```

## Verification commands

```bash
curl -s -o /dev/null -w "status: %{http_code}\n" -L "https://shop.example.com/products/trail-runner-boot-v1"
```

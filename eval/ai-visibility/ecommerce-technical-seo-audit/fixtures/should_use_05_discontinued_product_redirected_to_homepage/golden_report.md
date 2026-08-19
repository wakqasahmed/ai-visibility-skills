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

- `winter-parka-2023` returns a `301` whose final destination is the site's own root
  (`200 https://shop.example.com/`) — redirecting a discontinued product to the homepage risks
  being evaluated as a soft 404, discarding whatever ranking signal the old URL had built up.
- No direct successor product exists, but `mens-jackets` is a relevant category page — a
  closer, still-relevant redirect target than the homepage.

## Recommended fixes

Change the redirect target from the homepage to the closest relevant category, since there is
no direct product successor — items should redirect to items, categories to categories, never
to the homepage:

```
301 https://shop.example.com/products/winter-parka-2023 -> https://shop.example.com/collections/mens-jackets
```

## Verification commands

```bash
curl -s -o /dev/null -w "final URL after redirects: %{url_effective}\n" -L "https://shop.example.com/products/winter-parka-2023"
```

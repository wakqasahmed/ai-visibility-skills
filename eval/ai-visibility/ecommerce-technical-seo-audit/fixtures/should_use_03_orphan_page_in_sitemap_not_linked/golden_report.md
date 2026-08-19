## Sample scope

Sample of 1 product URL checked against the homepage + top 5 category pages' internal links,
out of an unknown total product/page count — this is a spot-check, not a full-catalog crawl.

## Thin category/collection page findings

Not checked in this sample — no category-page text was supplied.

## Faceted-navigation duplicate URL findings

Not checked in this sample — no filter/sort variant was supplied.

## Orphan page findings

- `trail-runner-boot-legacy` is present in `sitemap.xml` (`<loc>` entry confirmed) but does not
  appear anywhere in the internal-link set gathered from the homepage or the 5 sampled category
  pages — a candidate orphan page.
- Its `sitemap.xml` presence alone does not rule out being an orphan: sitemap entries and
  internal links are independent signals, and only the link-crawl comparison above found the gap.
- Before treating this as confirmed, check a few more plausible entry points (search results,
  the `trail-runner-boot` related-products `href`) not covered in this sample's link crawl.

## Discontinued-product handling findings

Not checked in this sample — no HTTP status/redirect data was supplied for this URL.

## Recommended fixes

Add at least one internal link to `trail-runner-boot-legacy` from a relevant page — ideally the
current `trail-runner-boot`'s related-products block or its parent category — so it stops
depending solely on the sitemap and an external/direct link for discovery:

```html
<a href="/products/trail-runner-boot-legacy">Trail Runner Boot (Legacy)</a>
```

## Verification commands

```bash
curl -s "https://shop.example.com/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | grep "trail-runner-boot-legacy"
curl -s "https://shop.example.com/products/trail-runner-boot" | grep -o 'href="[^"]*trail-runner-boot-legacy[^"]*"'
```

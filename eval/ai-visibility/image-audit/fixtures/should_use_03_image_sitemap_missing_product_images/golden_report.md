## Alt text coverage and quality summary

Not checked in this request — no `<img>` tag markup (with or without `alt`) was provided.

## Image sitemap coverage summary

- Neither `desk-lamp-main.jpg` nor `desk-lamp-detail.jpg` appears as an `image:loc` entry under the `desk-lamp` page's `<url>` block in `sitemap.xml` — the `<url>` block has no `image:image` tags at all, even though a sibling page (`ceramic-mug`) correctly declares one.
- 0 of 2 images on this product page have a matching `image:loc` entry — full coverage gap for this `<url>` block.

## ImageObject schema presence and completeness

Not checked in this request — no JSON-LD was provided or fetched.

## Fetchability findings

Not checked in this request — no lazy-load markup or direct image fetch status was provided.

## Recommended fixes

Add `image:image`/`image:loc` entries for both product images to the `desk-lamp` `<url>` block, matching the pattern already used for `ceramic-mug`:

```xml
<url>
  <loc>https://shop.example.com/products/desk-lamp</loc>
  <image:image>
    <image:loc>https://shop.example.com/img/desk-lamp-main.jpg</image:loc>
  </image:image>
  <image:image>
    <image:loc>https://shop.example.com/img/desk-lamp-detail.jpg</image:loc>
  </image:image>
</url>
```

Check whether this is a per-product gap or a template-wide one — if the sitemap generator only emits `image:image` for some product templates, other product pages likely have the same coverage gap.

## Verification commands

```bash
curl -s "https://shop.example.com/sitemap.xml" | grep -oE '<image:loc>[^<]*</image:loc>'
curl -s "https://shop.example.com/products/desk-lamp" | grep -oiE '<img[^>]+src="[^"]*"'
```

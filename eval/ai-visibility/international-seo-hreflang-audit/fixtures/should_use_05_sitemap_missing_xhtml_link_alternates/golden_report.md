# International SEO & Hreflang Audit Report

## Target Locale Matrix

| Locale | URL | Status | Canonical Target |
|---|---|:---:|---|
| `en` | `https://example.com/` | `200` | `https://example.com/` |
| `es` | `https://example.com/es/` | `200` | `https://example.com/es/` |
| `de` | `https://example.com/de/` | `200` | `https://example.com/de/` |

## Hreflang Conformance and Reciprocity

- HTML header tags are present, but XML sitemap `sitemap.xml` contains standard `<url><loc>` entries without `<xhtml:link rel="alternate" hreflang="..." href="...">` annotations `[GOOGLE-HREFLANG-01]`. Localized sitemaps accelerate search crawler discovery for international variations across large sites.

## Canonical Alignment

- All localized pages maintain distinct self-referential canonical tags.

## Recommended Fixes

1. Add `xmlns:xhtml="http://www.w3.org/1999/xhtml"` to `<urlset>` and nest `xhtml:link` annotations under each `<url>` entry:
   ```xml
   <url>
     <loc>https://example.com/</loc>
     <xhtml:link rel="alternate" hreflang="en" href="https://example.com/" />
     <xhtml:link rel="alternate" hreflang="es" href="https://example.com/es/" />
     <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/" />
   </url>
   ```

## Verification Commands

```bash
curl -s "https://example.com/sitemap.xml" | grep -i "xhtml:link"
# Expected: <xhtml:link rel="alternate" ... />
```

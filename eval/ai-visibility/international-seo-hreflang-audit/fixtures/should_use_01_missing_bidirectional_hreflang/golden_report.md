# International SEO & Hreflang Audit Report

## Target Locale Matrix

| Locale | URL | Status | Canonical Target |
|---|---|:---:|---|
| `en` | `https://example.com/en/product` | `200` | `https://example.com/en/product` |
| `es` | `https://example.com/es/producto` | `200` | `https://example.com/es/producto` |

## Hreflang Conformance and Reciprocity

- **Origin Page (`/en/product`)**: Declares `hreflang="en"` pointing to itself and `hreflang="es"` pointing to `https://example.com/es/producto` `[GOOGLE-HREFLANG-01]`.
- **Target Page (`/es/producto`)**: Missing reciprocal `hreflang="en"` return tag. Search engines ignore alternate associations when reciprocity is broken.

## Canonical Alignment

- Both pages correctly declare self-referential canonical tags:
  - `https://example.com/en/product` → `<link rel="canonical" href="https://example.com/en/product">`
  - `https://example.com/es/producto` → `<link rel="canonical" href="https://example.com/es/producto">`

## Recommended Fixes

1. Add reciprocal `hreflang="en"` alternate tag to `<head>` on `https://example.com/es/producto`:
   ```html
   <link rel="alternate" hreflang="en" href="https://example.com/en/product" />
   <link rel="alternate" hreflang="es" href="https://example.com/es/producto" />
   ```

## Verification Commands

```bash
curl -s "https://example.com/es/producto" | grep -i 'hreflang="en"'
# Expected: <link rel="alternate" hreflang="en" href="https://example.com/en/product" />
```

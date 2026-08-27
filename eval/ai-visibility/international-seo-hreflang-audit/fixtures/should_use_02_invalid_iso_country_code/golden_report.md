# International SEO & Hreflang Audit Report

## Target Locale Matrix

| Locale | URL | Status | Canonical Target |
|---|---|:---:|---|
| `en-US` | `https://example.com/us/` | `200` | `https://example.com/us/` |
| `en-UK` (Invalid) | `https://example.com/uk/` | `200` | `https://example.com/uk/` |

## Hreflang Conformance and Reciprocity

- **Invalid Country Code**: The tag specifies `hreflang="en-UK"`. Under ISO 3166-1 alpha-2, the code for the United Kingdom is `GB` (Great Britain), not `UK` `[W3C-ISO-LANG-01]`. Search crawlers will fail to recognize `en-UK` as a valid locale tag `[GOOGLE-HREFLANG-01]`.

## Canonical Alignment

- Self-referential canonical tags are in place on all regional pages.

## Recommended Fixes

1. Update all `<link rel="alternate" hreflang="...">` references from `en-UK` to `en-GB`:
   ```html
   <link rel="alternate" hreflang="en-GB" href="https://example.com/uk/" />
   ```

## Verification Commands

```bash
curl -s "https://example.com/uk/" | grep -i "hreflang"
# Expected: <link rel="alternate" hreflang="en-GB" href="https://example.com/uk/" />
```

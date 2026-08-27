# International SEO & Hreflang Audit Report

## Target Locale Matrix

| Locale | URL | Status | Canonical Target |
|---|---|:---:|---|
| `es` | `https://example.com/es/` | `200` | `https://example.com/es/` |
| `de` | `https://example.com/de/` | `200` | `https://example.com/de/` |
| `fr` | `https://example.com/fr/` | `200` | `https://example.com/fr/` |
| Global Fallback | `https://example.com/` | `200` | `https://example.com/` |

## Hreflang Conformance and Reciprocity

- **Missing x-default Fallback**: Language-specific tags (`es`, `de`, `fr`) are declared, but there is no `hreflang="x-default"` declaration `[GOOGLE-HREFLANG-01]`. Without `x-default`, users from un-targeted locales (e.g. English, Italian, Japanese) or language selectors are not routed to a designated default landing page.

## Canonical Alignment

- Each localized page correctly points to its own URL as canonical.

## Recommended Fixes

1. Add the `x-default` alternate link tag to all localized header templates pointing to the root global landing page:
   ```html
   <link rel="alternate" hreflang="x-default" href="https://example.com/" />
   ```

## Verification Commands

```bash
curl -s "https://example.com/" | grep -i 'hreflang="x-default"'
# Expected: <link rel="alternate" hreflang="x-default" href="https://example.com/" />
```

# International SEO & Hreflang Audit Report

## Target Locale Matrix

| Locale | URL | Status | Canonical Target |
|---|---|:---:|---|
| `en` | `https://example.com/` | `200` | `https://example.com/` |
| `fr` | `https://example.com/fr/` | `200` | `https://example.com/` (Conflicting) |

## Hreflang Conformance and Reciprocity

- Hreflang tags are declared on both pages for `en` and `fr` `[GOOGLE-HREFLANG-01]`.

## Canonical Alignment

- **Critical Canonical Conflict**: On `https://example.com/fr/`, the `<link rel="canonical">` points to the root `https://example.com/` instead of self-referencing `https://example.com/fr/`.
- Per Google guidelines `[GOOGLE-HREFLANG-01]`, a canonical tag instructing search engines to index the root page directly contradicts the `hreflang` tag instructing them to index the French alternate. This causes the localized page to be dropped from search indices.

## Recommended Fixes

1. Update the canonical tag on `https://example.com/fr/` to point to itself:
   ```html
   <link rel="canonical" href="https://example.com/fr/" />
   ```

## Verification Commands

```bash
curl -s "https://example.com/fr/" | grep -i 'rel="canonical"'
# Expected: <link rel="canonical" href="https://example.com/fr/" />
```

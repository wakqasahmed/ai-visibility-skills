# Paywall & Subscription Content Access Audit Report

## Paywall Specification Conformance Matrix

| Property | Status | Value / Selector |
|---|:---:|---|
| `isAccessibleForFree` | `MISSING` | Not declared in JSON-LD |
| `hasPart` | `MISSING` | No `WebPageElement` paywall selector |
| Schema Type | `NewsArticle` | Present |

- **Missing Paywall Structured Data**: The page renders a subscription paywall, but lacks `isAccessibleForFree: "False"` and `hasPart` JSON-LD schema markup `[GOOGLE-PAYWALL-SCHEMA-01] [SCHEMA-ISACCESSIBLEFORFREE-01]`. Without this, search and AI crawlers risk classifying the paywall modal as cloaking or thin content.

## Lead-In Snippet Renderability and Visibility

- The headline, author, date, and introductory lead paragraph (180 words) render in the initial server HTML payload.

## AI Crawler Policy Separation

- `robots.txt` permits `OAI-SearchBot` and `PerplexityBot` while disallowing bulk training crawlers (`GPTBot`, `Google-Extended`).

## Recommended Fixes

1. Add `isAccessibleForFree: "False"` and `hasPart` to the `NewsArticle` JSON-LD schema:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "NewsArticle",
     "headline": "Premium Market Analysis",
     "isAccessibleForFree": "False",
     "hasPart": {
       "@type": "WebPageElement",
       "isAccessibleForFree": "False",
       "cssSelector": ".paywall-gated-body"
     }
   }
   ```

## Verification Commands

```bash
curl -s "https://news.example.com/premium-article" | grep -i "isAccessibleForFree"
# Expected: "isAccessibleForFree": "False"
```

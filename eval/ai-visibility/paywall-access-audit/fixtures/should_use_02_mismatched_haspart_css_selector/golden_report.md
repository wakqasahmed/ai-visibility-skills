# Paywall & Subscription Content Access Audit Report

## Paywall Specification Conformance Matrix

| Property | Status | Value / Selector |
|---|:---:|---|
| `isAccessibleForFree` | `PASS` | `False` |
| `hasPart.cssSelector` | `INVALID` | `.gated-article-text` (DOM class: `.premium-body`) |

- **Mismatched CSS Selector**: The schema declares `hasPart.cssSelector: ".gated-article-text"`, but the actual HTML DOM uses class `.premium-body` `[GOOGLE-PAYWALL-SCHEMA-01]`. Google and AI search crawlers cannot match the structured declaration to the gated content section.

## Lead-In Snippet Renderability and Visibility

- Public executive summary is rendered server-side and visible to search bots.

## AI Crawler Policy Separation

- Bot policies correctly allow search citation crawlers.

## Recommended Fixes

1. Update the `cssSelector` property in JSON-LD to match the actual DOM class `.premium-body`:
   ```json
   "hasPart": {
     "@type": "WebPageElement",
     "isAccessibleForFree": "False",
     "cssSelector": ".premium-body"
   }
   ```

## Verification Commands

```bash
curl -s "https://research.example.com/reports/ai-trends" | grep -i 'cssSelector'
# Expected: "cssSelector": ".premium-body"
```

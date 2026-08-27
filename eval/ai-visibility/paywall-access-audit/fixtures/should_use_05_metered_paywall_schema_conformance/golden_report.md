# Paywall & Subscription Content Access Audit Report

## Paywall Specification Conformance Matrix

| Property | Status | Value / Selector |
|---|:---:|---|
| `isAccessibleForFree` | `MISSING` | Not declared in JSON-LD |
| `hasPart.cssSelector` | `MISSING` | No selector |
| Access Model | Metered (3 free/mo) | Structured Data Required |

- **Metered Paywall Structured Data Requirement**: Per Google Search Central guidelines `[GOOGLE-PAYWALL-SCHEMA-01]`, metered paywalls (such as granting N free articles before paywalling) must still include `isAccessibleForFree: "False"` and `hasPart` markup to distinguish the metering barrier from cloaking.

## Lead-In Snippet Renderability and Visibility

- Full article text is initially delivered in HTML, gated by client-side metering cookie checks.

## AI Crawler Policy Separation

- `robots.txt` correctly allows standard search crawlers.

## Recommended Fixes

1. Add `isAccessibleForFree: "False"` and `hasPart` to all metered `NewsArticle` schema templates `[GOOGLE-PAYWALL-SCHEMA-01] [SCHEMA-ISACCESSIBLEFORFREE-01]`.

## Verification Commands

```bash
curl -s "https://example.com/article" | grep -i "isAccessibleForFree"
# Expected: "isAccessibleForFree": "False"
```

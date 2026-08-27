# Paywall & Subscription Content Access Audit Report

## Paywall Specification Conformance Matrix

| Property | Status | Value / Selector |
|---|:---:|---|
| `isAccessibleForFree` | `PASS` | `False` |
| `hasPart.cssSelector` | `PASS` | `.article-gated` |

## Lead-In Snippet Renderability and Visibility

- Public preview paragraphs render cleanly in server HTML.

## AI Crawler Policy Separation

- **Accidental Search Bot Blocking**: In `robots.txt`, the site has `User-agent: * Disallow: /` and explicitly blocks `OAI-SearchBot` and `PerplexityBot`.
- Blocking citation bots prevents search engines from indexing public lead-in snippets and quoting article conclusions with backlink citations.

## Recommended Fixes

1. Distinguish training crawlers from search citation bots in `robots.txt`:
   ```txt
   # Block AI foundation training
   User-agent: GPTBot
   Disallow: /
   
   User-agent: Google-Extended
   Disallow: /
   
   # Allow AI search citation and indexing
   User-agent: OAI-SearchBot
   Allow: /
   
   User-agent: PerplexityBot
   Allow: /
   ```

## Verification Commands

```bash
curl -s "https://example.com/robots.txt" | grep -A 2 -i "OAI-SearchBot"
# Expected: Allow: /
```

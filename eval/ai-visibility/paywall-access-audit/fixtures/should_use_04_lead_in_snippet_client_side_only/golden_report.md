# Paywall & Subscription Content Access Audit Report

## Paywall Specification Conformance Matrix

| Property | Status | Value / Selector |
|---|:---:|---|
| `isAccessibleForFree` | `PASS` | `False` |
| `hasPart.cssSelector` | `PASS` | `.subscriber-only` |

## Lead-In Snippet Renderability and Visibility

- **Client-Side Teaser Rendering Blocker**: The free lead paragraph is loaded dynamically via client-side JavaScript API calls after page load. In the raw server HTML payload, the content body is completely empty.
- Non-JS executing search crawlers see zero textual content, triggering soft-404 / thin-content penalties.

## AI Crawler Policy Separation

- `robots.txt` directives correctly allow search indexing bots.

## Recommended Fixes

1. Server-render the first 150–250 words (lead paragraph, headline, author) directly in the static HTML response before injecting the client-side paywall gate.

## Verification Commands

```bash
curl -s "https://newsletter.example.com/post/1" | grep -oiE '<p[^>]*>[^<]+'
# Expected: <p>First paragraph of article text...</p>
```

# International SEO & Hreflang Audit Report: spa-store.com

## Target Locale Matrix

| Locale | URL | Status | Canonical Target |
|---|---|:---:|---|
| `en` | `https://spa-store.com/en/shop` | `200` | `https://spa-store.com/en/shop` |
| `fr` | `https://spa-store.com/fr/shop` | `200` | `https://spa-store.com/fr/shop` |

## Hreflang Conformance and Reciprocity

- **Raw HTML Pass**: 0 `<link rel="alternate" hreflang="...">` tags observed in the initial HTTP response.
- **Hydrated DOM Pass (`--dump-dom`)**: React Helmet (`data-react-helmet="true"`) injects `hreflang="en"` and `hreflang="fr"` tags upon client-side JavaScript execution `[GOOGLE-HREFLANG-01]`.
- **Finding**: **Present in the rendered DOM but absent from the initial server response** — invisible to non-JS-executing search and AI citation crawlers (ClaudeBot, GPTBot, PerplexityBot).

## Canonical Alignment

- Self-referential canonical tags are also injected via React Helmet at runtime.

## Recommended Fixes

1. Move hreflang alternate declarations to server-rendered HTML or emit HTTP `Link:` headers at the edge CDN (Cloudflare/Fastly):
   ```http
   Link: <https://spa-store.com/en/shop>; rel="alternate"; hreflang="en", <https://spa-store.com/fr/shop>; rel="alternate"; hreflang="fr"
   ```

## Verification Commands

```bash
# Compare raw HTML with headless DOM dump
curl -s "https://spa-store.com/en/shop" | grep -i "hreflang"
chromium --headless=new --dump-dom "https://spa-store.com/en/shop" | grep -i "hreflang"
```

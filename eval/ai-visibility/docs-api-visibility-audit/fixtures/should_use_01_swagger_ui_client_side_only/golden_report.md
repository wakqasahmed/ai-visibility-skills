# Developer Documentation & API Visibility Audit Report

## API Schema Discovery Matrix

| Path | Status | Format | Parseable |
|---|:---:|---|:---:|
| `https://api.example.com/openapi.json` | `200` | OpenAPI 3.1.0 | Yes (34 endpoints) |
| `https://api.example.com/docs` | `200` | HTML SPA Shell | Empty in raw HTML |

## Documentation Renderability and SSR Conformance

- **Client-Side Rendering Blocker**: The documentation portal at `/docs` serves a client-side SPA bundle (`<div id="swagger-ui"></div>`) without server-side rendering `[OPENAPI-SPEC-01]`.
- AI search bots and non-JS executing coding assistants (Claude Code, Cursor) see an empty HTML shell, preventing automatic endpoint comprehension.

## Code Sample and Syntax Markup Quality

- Code blocks inside the client-side UI lack static HTML fallback.

## Recommended Fixes

1. Expose a direct machine-readable link to `/openapi.json` in the `<head>` and footer:
   ```html
   <link rel="describedby" type="application/json" href="/openapi.json" />
   ```
2. Enable static site generation (SSG) or server-side rendering for API reference endpoints.

## Verification Commands

```bash
curl -s "https://api.example.com/docs" | grep -i "swagger-ui"
# Expected: <div id="swagger-ui"></div>
curl -s "https://api.example.com/openapi.json" | grep -i '"openapi":'
# Expected: "openapi": "3.1.0"
```

# Developer Documentation & API Visibility Audit Report

## API Schema Discovery Matrix

| Path | Status | Format | Parseable |
|---|:---:|---|:---:|
| `https://example.com/openapi.json` | `404` | None | N/A |
| `https://example.com/swagger.json` | `404` | None | N/A |
| `https://example.com/.well-known/openapi.json` | `404` | None | N/A |

## Documentation Renderability and SSR Conformance

- Documentation pages render in static HTML, but no raw machine-readable JSON/YAML API specification is hosted or advertised `[OPENAPI-SPEC-01]`.

## Code Sample and Syntax Markup Quality

- Code snippets exist but are written in prose rather than structured schema models.

## Recommended Fixes

1. Export and host a standardized OpenAPI 3.1 schema at `/openapi.json`:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" "https://example.com/openapi.json"
   ```
2. Reference the specification in `llms.txt` and HTML `<head>`.

## Verification Commands

```bash
curl -sI "https://example.com/openapi.json" | grep -i "HTTP/"
# Expected: HTTP/2 200
```

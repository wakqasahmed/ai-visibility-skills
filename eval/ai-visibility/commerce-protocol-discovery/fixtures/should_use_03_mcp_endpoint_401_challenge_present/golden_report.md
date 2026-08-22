## Site-type classification

Classified as ecommerce: `Product` JSON-LD on merch pages and an "Add to cart" affordance.

## UCP business profile

- `curl -s -o /dev/null -w "%{http_code}\n" "https://tools.example.org/.well-known/ucp"` →
  `404` — no UCP business profile discoverable at the standard endpoint.

## A2A Agent Card

- `curl -s -o /dev/null -w "%{http_code}\n" "https://tools.example.org/.well-known/agent-card.json"`
  → `404` — no A2A Agent Card discoverable at the standard endpoint.

## MCP

A remote MCP endpoint was claimed at `https://mcp.tools.example.org/mcp`, so its actual
challenge was inspected rather than guessing a site-root manifest:

- `curl -sI "https://mcp.tools.example.org/mcp"` → `401 Unauthorized`, with a
  `WWW-Authenticate: Bearer resource_metadata="https://mcp.tools.example.org/.well-known/oauth-protected-resource"`
  header — the endpoint advertises OAuth Protected Resource Metadata discovery per its own
  challenge.

## Catalog feeds

- `/products.json` and `/catalog.json` were not found, and `robots.txt` has no feed reference —
  no machine-readable catalog feed discoverable.

Full commerce-protocol readiness scoring and remediation is a separate audit capability — this
section only reports what's discoverable, not whether it's implemented correctly or safely.

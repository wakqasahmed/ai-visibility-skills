## Site-type classification

Classified as ecommerce/marketplace: `Product` schema present and a `/cart` checkout flow.

## UCP business profile

- `curl -s -o /dev/null -w "%{http_code}\n" "https://store.example.net/.well-known/ucp"` →
  `404` — no UCP business profile discoverable at the standard endpoint.

## A2A Agent Card

- `curl -s -o /dev/null -w "%{http_code}\n" "https://store.example.net/.well-known/agent-card.json"`
  → `404` — no A2A Agent Card discoverable at the standard endpoint.

## MCP

No MCP endpoint was claimed or discoverable, so no probe was run.

## Catalog feeds

- `curl -s -o /dev/null -w "%{http_code}\n" "https://store.example.net/products.json"` → `200`
  — a platform-native catalog listing is discoverable, item `991` ("Trail Runner Backpack 22L")
  sampled.
- Sampled item's feed price (`$89.00`) does not match the live product page's observed price
  (`$109.00`) — a stale-feed discrepancy, reported as observed evidence.

Full commerce-protocol readiness scoring and remediation is a separate audit capability — this
section only reports what's discoverable, not whether it's implemented correctly or safely.

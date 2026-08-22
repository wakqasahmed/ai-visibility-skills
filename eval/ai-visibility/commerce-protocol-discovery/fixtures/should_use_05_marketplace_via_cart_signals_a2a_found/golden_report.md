## Site-type classification

Classified as ecommerce/marketplace: no `Product`/`Offer` JSON-LD present, but a `/checkout`
flow, a `/cart` page, and "Add to cart" buttons on every listing are sufficient observable
signals.

## UCP business profile

- `curl -s -o /dev/null -w "%{http_code}\n" "https://marketplace.example.io/.well-known/ucp"` →
  `404` — no UCP business profile discoverable at the standard endpoint.

## A2A Agent Card

- `curl -s -o /dev/null -w "%{http_code}\n" "https://marketplace.example.io/.well-known/agent-card.json"`
  → `200` — an A2A Agent Card is discoverable, name `marketplace-example-agent`, version
  `1.0.0`.

## MCP

No MCP endpoint was claimed or discoverable, so no probe was run.

## Catalog feeds

- `curl -s -o /dev/null -w "%{http_code}\n" "https://marketplace.example.io/products.json"` →
  `404` — no machine-readable catalog feed discoverable at this checked location.

Full commerce-protocol readiness scoring and remediation is a separate audit capability — this
section only reports what's discoverable, not whether it's implemented correctly or safely.

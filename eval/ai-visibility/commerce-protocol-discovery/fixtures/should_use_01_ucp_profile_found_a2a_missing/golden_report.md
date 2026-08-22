## Site-type classification

Classified as ecommerce: `Product`/`Offer` JSON-LD present on product pages and an "Add to
Cart" button in the raw HTML.

## UCP business profile

- `curl -s -o /dev/null -w "%{http_code}\n" "https://shop.example.com/.well-known/ucp"` →
  `200` — a UCP business profile is discoverable at the standard endpoint.

## A2A Agent Card

- `curl -s -o /dev/null -w "%{http_code}\n" "https://shop.example.com/.well-known/agent-card.json"`
  → `404` — no A2A Agent Card discoverable at the standard endpoint.

## MCP

No MCP endpoint was claimed or discoverable anywhere on the site or in its docs, so no probe
was run — probing a site-root manifest path would be guessing, not observation.

## Catalog feeds

- `curl -s -o /dev/null -w "%{http_code}\n" "https://shop.example.com/products.json"` → `200` —
  a platform-native Shopify catalog listing is discoverable.

Full commerce-protocol readiness scoring and remediation is a separate audit capability — this
section only reports what's discoverable, not whether it's implemented correctly or safely.

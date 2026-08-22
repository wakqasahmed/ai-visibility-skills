## Site-type classification

Classified as ecommerce: `Product`/`Offer` JSON-LD on every product page and "Add to Cart"
buttons throughout.

## UCP business profile

- `curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/.well-known/ucp"` →
  `404` — no UCP business profile discoverable at the standard endpoint.

## A2A Agent Card

- `curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/.well-known/agent-card.json"`
  → `404` — no A2A Agent Card discoverable at the standard endpoint.

## MCP

No MCP endpoint was claimed or discoverable anywhere on the site, so no probe was run.

## Catalog feeds

- `curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/products.json"` →
  `404`
- `curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/catalog.json"` →
  `404`
- `robots.txt` references only `Sitemap: https://basicshop.example.com/sitemap.xml`, no feed
  reference — no machine-readable catalog feed discoverable at any checked location.

Full commerce-protocol readiness scoring and remediation is a separate audit capability — this
section only reports what's discoverable, not whether it's implemented correctly or safely.

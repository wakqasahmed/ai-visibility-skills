## Add Product JSON-LD to top 20 product pages

- Priority: P1 (important — blocks rich-result and citation parsing)
- Source finding: schema-markup-audit
- Acceptance criteria: each of the 20 sampled product URLs serves a `<script type="application/ld+json">` block with `@type: Product`, `name`, `offers.price`, `offers.availability`.
- Verification:
  ```bash
  curl -s "$URL" | grep -oE '<script type="application/ld\+json">.*?</script>'
  # expect: match containing "@type":"Product" (was: no match)
  ```
- Owner: engineering / CMS templating.

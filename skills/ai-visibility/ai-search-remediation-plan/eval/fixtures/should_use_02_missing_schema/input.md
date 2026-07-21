# Audit findings — schema-markup-audit

### Finding: No Product JSON-LD on top 20 product pages

- Severity: important
- Evidence: `schema-markup-audit` crawl of 20 sampled product URLs found zero `<script type="application/ld+json">` blocks with `@type: Product`.
- Source skill: schema-markup-audit
- Reference check: `curl -s "$URL" | grep -oE '<script type="application/ld\+json">.*?</script>'`

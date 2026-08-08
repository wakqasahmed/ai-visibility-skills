## Sitemap paths found

- `https://www.northfield-outfitters.example/robots.txt` contains no `Sitemap:` line.
- `https://www.northfield-outfitters.example/sitemap.xml` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `404`.
- `https://www.northfield-outfitters.example/sitemap_index.xml` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `404`.
- No sitemap exists anywhere on the site.

## Coverage gaps

- No sitemap means every page on `https://www.northfield-outfitters.example` is a coverage gap by default: `curl -s "https://www.northfield-outfitters.example/robots.txt" | grep -i "^sitemap"` returns no match, so crawlers have no declared, machine-readable list of URLs to discover.

## Broken or blocked URLs

- None found — this is a coverage-discovery failure, not a broken-URL issue.

## Canonical and redirect issues

- None found — no sitemap exists to evaluate canonical/redirect consistency against.

## Priority fixes

- Priority: P0 (critical) — publish a `sitemap.xml` at the site root listing all indexable public pages, and add a `Sitemap:` line to `robots.txt` pointing to it. Sitemap presence is not proof of indexing on its own, but its total absence removes a primary machine-readable discovery path crawlers rely on.

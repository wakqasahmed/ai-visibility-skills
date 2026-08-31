## Sitemap paths found

- `https://www.northfield-outfitters.example/robots.txt` → `curl -s "$SITE/robots.txt" | grep -iE "^[[:space:]]*sitemap:"` returns no match: no `Sitemap:` directive is declared.
- `https://www.northfield-outfitters.example/` → `curl -s "$SITE" | grep -oiE '<link[^>]+rel="sitemap"[^>]*>'` returns no match: the homepage `<head>` declares no sitemap either.
- Default-path probes, all `404` via `curl -s -o /dev/null -w "%{http_code}\n"`: `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml`, `/sitemap/sitemap-index.xml`, `/sitemap-0.xml`, `/wp-sitemap.xml`.
- No sitemap exists anywhere on the site — not declared, not linked, and not at any framework default path.

## Coverage gaps

- No sitemap means every page on `https://www.northfield-outfitters.example` is a coverage gap by default: neither the `robots.txt` directive check nor the homepage `rel="sitemap"` link check returns anything, and all six probed default paths return `404`, so crawlers have no declared, machine-readable list of URLs to discover.

## Broken or blocked URLs

- None found — this is a coverage-discovery failure, not a broken-URL issue.

## Canonical and redirect issues

- None found — no sitemap exists to evaluate canonical/redirect consistency against.

## Priority fixes

- Priority: P0 (critical) — publish a `sitemap.xml` at the site root listing all indexable public pages, and add a `Sitemap:` line to `robots.txt` pointing to it. Sitemap presence is not proof of indexing on its own, but its total absence removes a primary machine-readable discovery path crawlers rely on.

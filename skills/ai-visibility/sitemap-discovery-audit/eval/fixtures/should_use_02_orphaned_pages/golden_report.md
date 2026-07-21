## Sitemap paths found

- `https://www.driftwood-coffee.example/robots.txt` → `Sitemap: https://www.driftwood-coffee.example/sitemap.xml`.
- `https://www.driftwood-coffee.example/sitemap.xml` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `200`, well-formed XML, 142 `<url>` entries.

## Coverage gaps

- `comm -23 /tmp/nav-links.txt /tmp/sitemap-links.txt` shows 18 published `/guides/*` URLs (e.g. `https://www.driftwood-coffee.example/guides/pour-over-ratios`) reachable from on-site navigation but absent from `sitemap.xml` — orphaned pages crawlers may never discover.

## Broken or blocked URLs

- None found among the 142 sitemap entries sampled.

## Canonical and redirect issues

- None found — sampled sitemap URLs return `200` with matching canonical tags.

## Priority fixes

- Priority: P1 (important) — add the 18 orphaned `/guides/*` URLs to `sitemap.xml`. Sitemap presence is not proof of indexing, but omission from the sitemap removes a primary discovery signal for these pages.

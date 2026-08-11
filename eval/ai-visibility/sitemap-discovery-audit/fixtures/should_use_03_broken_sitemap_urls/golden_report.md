## Sitemap paths found

- `https://www.harborline-tools.example/robots.txt` → `Sitemap: https://www.harborline-tools.example/sitemap.xml`.
- `https://www.harborline-tools.example/sitemap.xml` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `200`, well-formed XML, 340 `<url>` entries.

## Coverage gaps

- None found — sampled navigation links all appear in the sitemap.

## Broken or blocked URLs

- `https://www.harborline-tools.example/products/discontinued-hand-drill` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `404`, still listed in `sitemap.xml`.
- `https://www.harborline-tools.example/products/legacy-wrench-set` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `500`, still listed in `sitemap.xml`.

## Canonical and redirect issues

- None found among URLs that returned `200`.

## Priority fixes

- Priority: P1 (important) — remove `https://www.harborline-tools.example/products/discontinued-hand-drill` and `https://www.harborline-tools.example/products/legacy-wrench-set` from `sitemap.xml`, or fix the underlying `404`/`500` responses. Sitemap presence is not proof of indexing, and serving broken URLs in the sitemap wastes crawl budget on dead pages.

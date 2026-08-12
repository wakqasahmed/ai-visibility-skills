## Sitemap paths found

- `https://www.pinecrest-mattress.example/robots.txt` → `Sitemap: https://www.pinecrest-mattress.example/sitemap.xml`.
- `https://www.pinecrest-mattress.example/sitemap.xml` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `200`, well-formed XML, `curl -s "https://www.pinecrest-mattress.example/sitemap.xml" | grep -c '<url>'` returns `40000` entries.

## Coverage gaps

- None found — the ~120 real product/category pages are all present in the sitemap.

## Broken or blocked URLs

- None found among sampled entries — the volume issue is generated-URL noise, not broken links.

## Canonical and redirect issues

- `https://www.pinecrest-mattress.example/mattresses?size=queen&firmness=medium&color=grey` and thousands of similar faceted filter-combination URLs are listed in `sitemap.xml`; `curl -s "https://www.pinecrest-mattress.example/mattresses?size=queen&firmness=medium&color=grey" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'` shows each one canonicalizes back to `https://www.pinecrest-mattress.example/mattresses`, so the sitemap is dominated by low-value generated URLs pointing at the same canonical target.

## Priority fixes

- Priority: P2 (moderate) — exclude faceted/parameterized filter-combination URLs from `sitemap.xml`; they self-canonicalize to `/mattresses` and add crawl noise rather than distinct indexable pages. `curl -s "https://www.pinecrest-mattress.example/sitemap.xml" | grep -oE '<lastmod>[^<]+</lastmod>' | sort -u | tail -20` also shows most entries share one stale `lastmod` value from over a year ago, so freshness signal is unreliable. Sitemap presence is not proof of indexing — a 40,000-entry sitemap dominated by generated URLs and stale lastmod values is lower-quality signal than a small, accurate one covering the ~120 real pages.

## Sitemap paths found

- `https://www.pinegate-outfitters.example/robots.txt` → `Sitemap: https://www.pinegate-outfitters.example/sitemap.xml`.
- `https://www.pinegate-outfitters.example/sitemap.xml` → `curl -s -o /dev/null -w "%{http_code}\n"` returns `200`, well-formed XML.

## Coverage gaps

- None found — the page in question is present in the sitemap.

## Broken or blocked URLs

- `https://www.pinegate-outfitters.example/gear/alpine-tent-3p` — `curl -s -o /dev/null -w "%{http_code}\n" https://www.pinegate-outfitters.example/gear/alpine-tent-3p` returns `500`, confirming the server error reported in the request.

## Canonical and redirect issues

- None found for this URL beyond the 500 status noted above.

## Priority fixes

- Priority: P0 (immediate) — `https://www.pinegate-outfitters.example/gear/alpine-tent-3p` is listed in `sitemap.xml` with `lastmod` `2026-08-05`, which is 14 days before reference audit (2026-08-19), not after it. Per the chronological date arithmetic guardrail, the sitemap's own timestamp only proves the entry existed as of 2026-08-05 — it does not establish when the 500 error began, and it is not evidence the page broke "after" this audit; the safest read is broken at time of this audit, exact break date unknown. Sitemap presence and a `lastmod` value are not proof of current indexing or freshness; confirm live status via the direct request above before reporting a break date.

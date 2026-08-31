## Sitemap paths found

- `https://tidewater-studio.example/robots.txt` → `curl -s "$SITE/robots.txt" | grep -iE "^[[:space:]]*sitemap:"` returns no match: the file exists but declares no `Sitemap:` directive.
- `https://tidewater-studio.example/` → `curl -s "$SITE" | grep -oiE '<link[^>]+rel="sitemap"[^>]*>'` returns `<link rel="sitemap" type="application/xml" href="/sitemap-index.xml">`. The site does declare its sitemap, in the homepage `<head>`.
- `https://tidewater-studio.example/sitemap-index.xml` → `200`, `content-type: application/xml`. This is `gatsby-plugin-sitemap`'s default output path; it is a sitemap index chaining to `https://tidewater-studio.example/sitemap-0.xml` (`200`, 75 `<loc>` entries).
- `https://tidewater-studio.example/sitemap.xml` → `404` and `https://tidewater-studio.example/sitemap_index.xml` → `404`. Those two paths are simply not what this generator writes; probing only them is what produced the earlier "no sitemap" conclusion.

You do have a sitemap, and crawlers that read the homepage `<head>` will find it.

## Coverage gaps

- `https://tidewater-studio.example/robots.txt` has no `Sitemap:` line (`curl -s "$SITE/robots.txt"` shows only `User-agent: *` and `Allow: /`). Any crawler that reads `robots.txt` and does not parse the homepage `<head>` has no pointer to `/sitemap-index.xml` — this is the actual discovery gap, narrower than "no sitemap".

## Broken or blocked URLs

- All 75 `<loc>` entries in `https://tidewater-studio.example/sitemap-0.xml` are written against `https://www.tidewater-studio.example/...`, and that host does not serve the site: `curl -s -o /dev/null -m 10 -w "%{http_code}" https://www.tidewater-studio.example/` fails to connect (TLS handshake times out against the S3 website-endpoint addresses it resolves to). Every URL a crawler takes from this sitemap is therefore unreachable.

## Canonical and redirect issues

- Host mismatch: the sitemap's `<loc>` host (`https://www.tidewater-studio.example`) differs from both the working host and the canonical host — `curl -s "https://tidewater-studio.example/" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'` returns `<link rel="canonical" href="https://tidewater-studio.example/">` (apex, `200`). The canonicals are right and the sitemap is wrong; there is no redirect from the `www` host to fall back on because that host does not serve HTTPS at all.

## Priority fixes

- Priority: P0 (critical) — rebuild the sitemap with the apex host so `<loc>` entries match the canonical, working host (`https://tidewater-studio.example/...`); in `gatsby-plugin-sitemap` this is the `siteMetadata.siteUrl` value. Until then every entry sends crawlers to a host that refuses connections.
- Priority: P1 — add `Sitemap: https://tidewater-studio.example/sitemap-index.xml` to `robots.txt` so the sitemap is discoverable without parsing the homepage `<head>`.
- Priority: P2 — either serve `www.tidewater-studio.example` with a valid certificate redirecting to the apex, or stop referencing it anywhere. Note that fixing discovery is not proof of indexing: sitemap presence does not guarantee any crawler or AI system indexes or cites these URLs.

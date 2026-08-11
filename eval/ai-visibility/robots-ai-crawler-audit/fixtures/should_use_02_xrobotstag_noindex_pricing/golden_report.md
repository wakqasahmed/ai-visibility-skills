## Current crawler policy summary

- `robots.txt` only disallows `/internal/`; the rest of the site, including
  `/pricing`, is crawlable by all named user-agents.
- No meta `robots` tag is present on `/pricing`.
- `Sitemap: https://example.com/sitemap.xml` is declared.

## Blocked high-value paths

- `/pricing` is blocked at the page level despite a permissive `robots.txt`:
  `curl -sI https://example.com/pricing` returns header
  `X-Robots-Tag: noindex, nofollow`, which most crawlers (including AI
  crawlers that honor `X-Robots-Tag`) treat as a hard block on indexing this
  page - `robots.txt` inspection alone would have missed this.

## AI crawler implications

- Any AI crawler or answer engine that respects `X-Robots-Tag` will exclude
  `/pricing` from its index even though it can technically fetch the page -
  the site's pricing information cannot be cited or summarized while this
  header is present.
- This is a page-level (HTTP header) rule, not a site-wide `robots.txt` rule,
  so it will not show up in a `robots.txt`-only audit.

## Recommended robots.txt changes

No `robots.txt` change is needed here since the block is not in `robots.txt`.
Remove the `X-Robots-Tag: noindex, nofollow` response header (or narrow it to
`nofollow` only if link-following is the real concern) at the origin/CDN
level for `/pricing`:

```
User-agent: *
Allow: /pricing
```

Confirming the site-wide `robots.txt` continues to `Allow: /pricing`
alongside removing the header improves the odds this page becomes
answer-engine visible - it does not guarantee citation or inclusion.

## Verification commands

```bash
curl -sI https://example.com/pricing | grep -i x-robots-tag
# expect: no output (was: "X-Robots-Tag: noindex, nofollow")
curl -s https://example.com/pricing | grep -oiE '<meta[^>]+robots[^>]+>'
```

## Current crawler policy summary

- `robots.txt` has no `Disallow` rules at all - fully permissive at the
  site-access level.
- `Sitemap` is declared and no `X-Robots-Tag` header is present on the docs
  page.
- The canonical tag on `/docs/getting-started` points to itself, which is
  correct.

## Blocked high-value paths

- `/docs/getting-started` is blocked at the HTML level despite a fully
  permissive `robots.txt`: `curl -s .../docs/getting-started | grep -oiE
  '<meta[^>]+robots[^>]+>'` returns `<meta name="robots" content="noindex,
  nofollow">`, which instructs any crawler that parses the page to exclude it
  from its index and not follow its links - `robots.txt` and header checks
  alone would have missed this.

## AI crawler implications

- Any AI crawler or answer engine that respects the meta robots tag will
  drop this docs page from its index and will not credit any outbound links
  from it, even though the page is fully fetchable - this likely explains
  the reported drop in AI-answer visibility for docs content.
- Because `robots.txt` shows no rule, this would be missed by a robots.txt-only
  audit; it required fetching and parsing the page itself.

## Recommended robots.txt changes

No `robots.txt` change is needed - the block is an HTML-level `meta robots`
tag, most likely a CMS template default applied to the docs section. Remove
or correct the tag at the template level so it no longer emits `noindex,
nofollow` for pages meant to be indexed, and confirm `robots.txt` continues
to allow the section:

```
User-agent: *
Allow: /docs/
```

Removing the incorrect meta tag improves the odds this page returns to AI
answers - it does not guarantee re-inclusion, since re-crawling and
re-indexing timing is controlled by each AI platform.

## Verification commands

```bash
curl -s https://example.com/docs/getting-started | grep -oiE '<meta[^>]+robots[^>]+>'
# expect: no output, or a tag without "noindex" (was: "noindex, nofollow")
```

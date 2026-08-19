## Current crawler policy summary

- `robots.txt` disallows `/account/` and `/checkout/` only; `/products/tide-lantern`
  and the rest of the catalog are crawlable by all named user-agents.
- `Sitemap: https://shoreline-goods.example/sitemap.xml` is declared.
- No page-level `noindex`/`X-Robots-Tag` block is present on the sampled product page.

## Blocked high-value paths

None found. `/account/` and `/checkout/` are the only disallowed paths in
`robots.txt`, and neither is a high-value discovery/answer page.

## AI crawler implications

- Crawler access itself is fine for `/products/tide-lantern`; the gap here is a
  response-header hygiene issue, not an access block.

## Security header gaps

- `https://shoreline-goods.example/products/tide-lantern` - `curl -sI ... | grep -i "strict-transport-security"` returns no output: `Strict-Transport-Security` is missing, so browsers are never told to force HTTPS on future visits to this origin.
- `https://shoreline-goods.example/products/tide-lantern` - `curl -sI ... | grep -i "x-content-type-options"` returns no output: `X-Content-Type-Options: nosniff` is missing, so a browser may MIME-sniff this response into an unintended content type.
- `https://shoreline-goods.example/products/tide-lantern` - `curl -sI ... | grep -i "x-frame-options"` returns no output: `X-Frame-Options` is missing (and no `Content-Security-Policy: frame-ancestors` was seen either), so the page can be framed by another site - a clickjacking risk.

## Recommended robots.txt changes

No `robots.txt` change is needed - the existing rules already stay permissive
where they should:

```
User-agent: *
Allow: /products/
Disallow: /account/
Disallow: /checkout/
```

The actual fix is response headers, not crawler directives. Add these headers
at the origin/CDN for all responses, including `/products/*`:

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

## Verification commands

```bash
curl -sI https://shoreline-goods.example/products/tide-lantern | grep -i "strict-transport-security"
curl -sI https://shoreline-goods.example/products/tide-lantern | grep -i "x-content-type-options"
curl -sI https://shoreline-goods.example/products/tide-lantern | grep -i "x-frame-options"
# expect all three to return a matching header line (currently: no output for any)
```

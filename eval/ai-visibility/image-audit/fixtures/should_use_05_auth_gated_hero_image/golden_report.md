## Alt text coverage and quality summary

Not checked in this request — no `<img>` tag markup was provided.

## Image sitemap coverage summary

Not checked in this request — no `sitemap.xml` was provided or fetched.

## ImageObject schema presence and completeness

Not checked in this request — no JSON-LD was provided or fetched.

## Fetchability findings

- The hero image URL `https://shop.example.com/img/homepage-hero.jpg` returns `403` on a direct, unauthenticated fetch and also returns `403` when fetched as `GPTBot`, while the page itself (`https://shop.example.com/`) returns `200` — the image is behind an auth/signed-URL or CDN gate even though the page it's embedded on is public. No AI crawler or vision-capable agent can fetch this image while the `403` persists.

## Recommended fixes

Serve the hero image from a publicly fetchable URL (remove the signed-URL/token requirement for this specific asset, or move it to a public CDN path) so it returns `200` for an unauthenticated request, the same status the page itself already returns:

```
# target: 200, unauthenticated, matching the page's own public access
curl -s -o /dev/null -w "%{http_code}\n" https://shop.example.com/img/homepage-hero.jpg
```

## Verification commands

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://shop.example.com/img/homepage-hero.jpg
curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://shop.example.com/img/homepage-hero.jpg
curl -s -o /dev/null -w "%{http_code}\n" -A "ClaudeBot" https://shop.example.com/img/homepage-hero.jpg
```

## Alt text coverage and quality summary

- `jacket.webp` (the product image) has no raw HTML `<img>` tag in the initial response; it is injected client-side via JavaScript with `alt="Winter Waterproof Jacket"`.

## Image sitemap coverage summary

Not checked in this request.

## ImageObject schema presence and completeness

Not checked in this request.

## Fetchability findings

- `jacket.webp` is **present in the rendered DOM but absent from initial server response** with no `<noscript>` fallback, making it invisible to non-JS vision crawlers.

## Recommended fixes

Add a server-rendered `<noscript>` fallback tag inside the image container:

```html
<noscript>
  <img src="https://cdn.spa-store.com/jacket.webp" alt="Winter Waterproof Jacket" />
</noscript>
```

## Verification commands

```bash
curl -s "https://spa-store.com/products/jacket" | grep -oiE '<img[^>]*>'
chromium --headless=new --dump-dom "https://spa-store.com/products/jacket" | grep -oiE '<img[^>]*>'
```

## Alt text coverage and quality summary

The hero image does carry a descriptive `alt="Hiking boots collection"` attribute — no finding here.

## Image sitemap coverage summary

Not checked in this request — no `sitemap.xml` was provided or fetched.

## ImageObject schema presence and completeness

Not checked in this request — no JSON-LD was provided or fetched.

## Fetchability findings

- The hero image `<img class="lazyload" data-src="...">` has no real `src` attribute — only `data-src`, which is populated by client-side JavaScript. No `<noscript>` fallback block exists anywhere on the page. Any crawler or agent that does not execute JavaScript (most AI crawlers, per `robots-ai-crawler-audit`'s bot list) will see an `<img>` tag with no fetchable image URL at all — this hero image is invisible to those agents regardless of how it renders in a JS-capable browser.

## Recommended fixes

Add a `<noscript>` fallback carrying the real image `src`, or switch to a native `loading="lazy"` attribute with a real `src` (which stays crawlable without executing JavaScript):

```html
<div class="hero">
  <img class="lazyload" data-src="https://shop.example.com/img/hiking-hero.jpg"
       src="https://shop.example.com/img/hiking-hero.jpg" loading="lazy"
       alt="Hiking boots collection">
  <noscript>
    <img src="https://shop.example.com/img/hiking-hero.jpg" alt="Hiking boots collection">
  </noscript>
</div>
```

This is likely a template-level fix — check whether the same lazy-load pattern without a fallback is used site-wide, since fixing it once in the template unblocks every page using it.

## Verification commands

```bash
curl -s "https://shop.example.com/categories/hiking-boots" | grep -oiE '<img[^>]*>' | grep -iE 'data-src|data-lazy|loading="lazy"'
curl -s "https://shop.example.com/categories/hiking-boots" | grep -ozE '<noscript>.*?</noscript>' | strings | grep -oiE '<img[^>]*src="[^"]*"'
```

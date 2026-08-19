## Alt text coverage and quality summary

- `boot-main.jpg` (the main product photo, `class="product-photo"`) has no `alt` attribute at all.
- `boot-side.jpg` and `boot-sole.jpg` (both `class="product-thumb"`) have no `alt` attribute either — 3 of 4 images on this page have no alt text.
- `cart-icon.svg` correctly uses `alt=""` since it's decorative — no finding there.

## Image sitemap coverage summary

Not checked in this request — no `sitemap.xml` was provided or fetched.

## ImageObject schema presence and completeness

Not checked in this request — no JSON-LD was provided or fetched.

## Fetchability findings

None found — all three product images use a real `src` attribute, so they are fetchable without JavaScript.

## Recommended fixes

Add a descriptive `alt` attribute to each non-decorative image, naming the product and the specific view shown:

```html
<img src="https://shop.example.com/img/boot-main.jpg" alt="Trail Runner Boot, front view" class="product-photo">
<img src="https://shop.example.com/img/boot-side.jpg" alt="Trail Runner Boot, side view" class="product-thumb">
<img src="https://shop.example.com/img/boot-sole.jpg" alt="Trail Runner Boot, sole tread detail" class="product-thumb">
```

Confirm each description actually matches what's shown before publishing — this audit cannot see the image content itself, so verify the specific view (front/side/sole) against the real photo.

## Verification commands

```bash
curl -s "https://shop.example.com/products/trail-runner-boot" | grep -oiE '<img[^>]*>' | grep -oiE 'alt="[^"]*"'
```

## Alt text coverage and quality summary

Not checked in this request — no `<img>` tag markup was provided.

## Image sitemap coverage summary

Not checked in this request — no `sitemap.xml` was provided or fetched.

## ImageObject schema presence and completeness

- `Product.image` is a bare URL string (`"https://shop.example.com/img/ceramic-mug.jpg"`) rather than a full `ImageObject`, even though the page has visible photo-credit metadata ("Photo: Jordan Lee") that a full `ImageObject`'s `creditText`/`author` could carry — per schema.org's `ImageObject` definition, `image` "can be a URL or a fully described ImageObject," and a bare URL leaves that visible credit unrepresented in structured data.

## Fetchability findings

Not checked in this request — no lazy-load markup or direct image fetch status was provided.

## Recommended fixes

Upgrade `image` to a full `ImageObject`, using only the credit text actually visible on the page:

```json
{
  "@type": "ImageObject",
  "url": "https://shop.example.com/img/ceramic-mug.jpg",
  "creditText": "Jordan Lee"
}
```

Do not add a `caption`, resolution, or photographer detail beyond "Jordan Lee" — nothing else about the image is visible on the page to verify against.

## Verification commands

```bash
curl -s "https://shop.example.com/products/ceramic-mug" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
```

Validate at https://validator.schema.org.

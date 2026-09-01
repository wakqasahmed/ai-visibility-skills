# Image audit check commands

Replace `$SITE` with the site origin and `$URL` with a representative page (product, category, or hero-image page).

## Alt text presence and quality

```bash
curl -s "$URL" | grep -oiE '<img[^>]*>' | grep -oiE 'alt="[^"]*"'
curl -s "$URL" | grep -oiE '<img(?!.*alt=)[^>]*>'
```

Per Google's image SEO documentation [GOOGLE-IMAGE-SEO-01], alt text should describe the
image concretely and in context — flag any `<img>` with no `alt` attribute, an empty
`alt=""` on a non-decorative image, or alt text that is generic/keyword-stuffed
(`"image"`, `"photo1"`, a repeated product-line keyword string) rather than descriptive.
An empty `alt=""` is only acceptable for genuinely decorative images.

## Image sitemap presence and coverage

```bash
curl -s "$SITE/robots.txt" | grep -i "^sitemap"
curl -s "$SITE/sitemap.xml" | grep -oE '<image:image>.*?</image:image>' 
curl -s "$SITE/sitemap.xml" | grep -oE '<image:loc>[^<]*</image:loc>'
curl -s "$SITE/sitemap.xml" | grep -c '<image:image>'
```

Per Google's image sitemap documentation [GOOGLE-IMAGE-SITEMAP-01], an image sitemap
declares images inside each `<url>` entry's `<image:image>`/`<image:loc>` tags (namespace
`xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"` on the `<urlset>` root),
up to 1,000 `<image:image>` entries per `<url>`, and images may be hosted on a different
domain (e.g. a CDN) than the page. Cross-check: extract the `<img src>` URLs actually
rendered on a sampled key page and confirm each one appears as an `<image:loc>` entry for
that page's `<url>` block — a key product/hero image present on the page but absent from
the sitemap is a coverage gap.

```bash
curl -s "$URL" | grep -oiE '<img[^>]+src="[^"]*"' | grep -oiE 'src="[^"]*"'
```

## `ImageObject` schema presence and completeness

```bash
curl -s "$URL" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
curl -s "$URL" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -c "
import json, sys
def find_image(o):
    if isinstance(o, dict):
        if 'image' in o:
            print(json.dumps(o['image']))
        for v in o.values():
            find_image(v)
    elif isinstance(o, list):
        for item in o:
            find_image(item)
for block in sys.stdin.read().split('\n'):
    try: find_image(json.loads(block))
    except Exception: pass
"
```

Per schema.org's `ImageObject` definition [SCHEMA-IMAGEOBJECT-01], an entity's `image`
property "can be a URL or a fully described `ImageObject`" — a bare string is valid but
carries no metadata. Flag a bare-URL `image` value on a `Product`, `Article`, or
`Organization` entity as weak (not broken) when the page has visible metadata a full
`ImageObject` could carry (caption, credit/author, or a specific width/height); recommend
upgrading to `{"@type": "ImageObject", "url": "...", "caption": "...", ...}` only using
metadata that is actually visible on the page — do not invent a caption or credit.

## Fetchability: JS-only lazy-load, auth, and geo-blocks

```bash
# Does the raw HTML contain a fetchable <img src> or only a JS-driven data-src/lazy attribute?
curl -s "$URL" | grep -oiE '<img[^>]*>' | grep -iE 'data-src|data-lazy|loading="lazy"'
curl -s "$URL" | grep -oiE '<img[^>]*>' | grep -iE 'src="[^"]+\.(jpg|jpeg|png|webp|gif|avif|svg)'

# Is there a <noscript> fallback carrying a real <img src>?
curl -s "$URL" | grep -ozE '<noscript>.*?</noscript>' | strings | grep -oiE '<img[^>]*src="[^"]*"'

# Fetch the image URL directly: confirm it's reachable without auth/geo-block
curl -s -o /dev/null -w "%{http_code}\n" "$IMAGE_URL"
curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" "$IMAGE_URL"
curl -s -o /dev/null -w "%{http_code}\n" -A "ClaudeBot" "$IMAGE_URL"

# Hydrated DOM cross-check when raw HTML has 0 images or missing alt attributes
CHROME=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium \
  || command -v chromium-browser || command -v microsoft-edge || true)
if [ -n "$CHROME" ]; then
  "$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$URL" > /tmp/hydrated_images.html
  grep -oiE '<img[^>]*>' /tmp/hydrated_images.html
else
  echo "no Chromium-family browser available, hydration cross-check not performed"
fi
```

An `<img>` whose only source is a `data-src`/`data-lazy` attribute set by JavaScript, with
no fallback `src` and no `<noscript><img src="...">` block, is unreachable to a crawler or
agent that does not execute JavaScript — flag this as a critical fetchability finding
regardless of how the image renders in a real browser. A non-200 status code on the direct
image fetch (401/403 auth-gated, 451/403 geo-blocked, or a redirect to a login page)
means the image cannot be fetched by an AI agent at all; report the exact status code
observed, per the evidence-discipline convention used across this skill pack — do not
infer a block without an observed status code or missing fallback markup.

## Verification

- Rich results / image eligibility: https://search.google.com/test/rich-results
- Generic schema validation: https://validator.schema.org
- Cross-check every alt-text, sitemap-coverage, and schema finding against the actual
  fetched HTML/sitemap/status code — do not assert a gap without the command output.

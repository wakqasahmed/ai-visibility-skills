## Sample scope

Sample of 2 category pages checked (`mens-running-shoes`, `womens-running-shoes`), out of an
unknown total category count — this is a spot-check, not a full-catalog crawl.

## Thin category/collection page findings

- `mens-running-shoes`: unique on-page text (outside nav/footer/product grid) is only the H1
  "Men's Running Shoes" — a 3-word count, no buying-guide or descriptive copy at all.
- `womens-running-shoes`: same word count pattern — unique text is only its own H1 (3 words),
  no editorial content.
- Both pages follow an identical `category-intro` template with a near-zero word count per
  category — a scaled duplication pattern, not just a single thin page.

## Faceted-navigation duplicate URL findings

Not checked in this sample — no filter/sort variant was supplied for these two category URLs.

## Orphan page findings

Not checked in this sample — no sitemap or navigation data was supplied.

## Discontinued-product handling findings

Not checked in this sample — no product URLs were supplied.

## Recommended fixes

Add a short (per practitioner guidance, roughly 150-300 words is a reasonable starting
target — not an official Google minimum) unique intro/buying-guide block per category, written
to that category's actual product range rather than reused boilerplate:

```html
<div class="category-intro">
  <h1>Men's Running Shoes</h1>
  <p>[unique copy specific to men's running shoes: fit notes, terrain guidance, size-range callout]</p>
</div>
```

## Verification commands

```bash
curl -s "https://shop.example.com/collections/mens-running-shoes" | python3 -c "
import re, sys
html = sys.stdin.read()
html = re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>', '', html, flags=re.S|re.I)
print(len(re.sub(r'<[^>]+>', ' ', html).split()))
"
```

## Existing schema types found

- `Article` with `headline` and `datePublished` at `https://blog.example.com/posts/composting-101`.

## Missing or weak schema

- `dateModified` is absent even though the page states it was last updated 2026-04-15.
- `author` is absent even though the page has a visible byline, "Priya Nair".
- `publisher` is absent even though the page states it is published by "Example Gardens".

## Mismatches with visible content

None found — `headline` and `datePublished` match the visible page content.

## Recommended JSON-LD changes

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Composting 101: A Beginner's Guide",
  "datePublished": "2026-03-01",
  "dateModified": "2026-04-15",
  "author": {
    "@type": "Person",
    "name": "Priya Nair"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Gardens"
  }
}
```

## Verification tools or commands

```bash
curl -s "https://blog.example.com/posts/composting-101" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
```

Validate at https://validator.schema.org; check rich-result eligibility separately at https://search.google.com/test/rich-results.

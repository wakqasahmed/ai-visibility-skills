## Current crawler policy summary

- `robots.txt` allows all crawlers to fetch `/research/market-report`, and the page
  has no `X-Robots-Tag` header.
- The page is indexable and self-canonical, but its meta robots tag sets the text
  snippet limit to zero.

## Blocked high-value paths

- `/research/market-report` returns `<meta name="robots" content="max-snippet:0">`,
  which prevents Google from showing a text snippet for this key page.

## AI crawler implications

- `max-snippet:0` is equivalent to `nosnippet` for Google. The page is not eligible
  to appear as a supporting link and its content cannot be used as direct input in
  Google AI Overviews or AI Mode while this directive is present.
- Blocking or allowing `Google-Extended` would not change this Google Search outcome;
  it is a separate control for other Google AI systems, not AI Overviews or AI Mode.

## Recommended robots.txt changes

No `robots.txt` change is needed. Because the stated goal is inclusion in Google's
AI features, remove `max-snippet:0` from the page template after confirming this is
not an intentional content policy. Removing it also permits classic Google Search
text snippets; there is no separate setting that enables AI-feature snippets while
suppressing classic snippets.

Keep the fetch policy permissive:

```
User-agent: *
Allow: /research/
```

This makes the page eligible for snippets but does not guarantee selection or
inclusion in an AI Overview or AI Mode response.

## Verification commands

```bash
curl -s https://example.com/research/market-report | grep -oiE '<meta[^>]+robots[^>]+>'
curl -sI https://example.com/research/market-report | grep -i '^x-robots-tag:'
curl -s https://example.com/research/market-report | grep -oiE '<(div|span|section)[^>]+data-nosnippet[^>]*>'
```

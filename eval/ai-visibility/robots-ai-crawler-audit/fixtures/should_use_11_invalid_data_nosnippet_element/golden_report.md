## Current crawler policy summary

- `robots.txt` allows all crawlers to fetch `/pricing`, and the page has no
  `X-Robots-Tag` header, no `<meta name="robots">`/`<meta name="googlebot">`
  snippet directive, and no `nosnippet`/`max-snippet` restriction of any kind.

## Blocked high-value paths

- `/pricing` has `data-nosnippet` on a `<p>` element (`200` on the page
  itself). This is **not an active snippet restriction**: Google only honors
  `data-nosnippet` on `div`, `span`, and `section`, so the price text remains
  fully eligible for a snippet, an AI Overview, or AI Mode.

## AI crawler implications

- The developer's change did not hide the price. Google's `data-nosnippet`
  documentation scopes the attribute to `div`/`span`/`section` only; placing
  it on any other element (here, `<p>`) is invalid markup with no effect on
  snippet eligibility.
- To actually exclude this text, wrap it in a `<span data-nosnippet>` or
  `<div data-nosnippet>` instead of relying on the attribute alone.

## Recommended robots.txt changes

No `robots.txt` change applies or would help here — this is a page-level
markup issue, not a crawl-access issue:

```
User-agent: *
Allow: /
```

If the intent is genuinely to exclude the price from snippets, move
`data-nosnippet` onto a `<span>` or `<div>` wrapping the price text; if the
intent was accidental, no change is needed since the current markup already
has no effect.

## Verification commands

```bash
curl -s https://example.com/pricing | grep -oiE '<[^>]+data-nosnippet[^>]*>'
curl -sI https://example.com/pricing | grep -i x-robots-tag
```

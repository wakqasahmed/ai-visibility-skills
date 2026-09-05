## Current crawler policy summary

- `robots.txt` allows all crawlers to fetch `/catalog/flagship-widget`, and
  the page has no `X-Robots-Tag` header.
- The page is indexable and self-canonical, but its Google-specific meta tag
  sets a `nosnippet` directive.

## Blocked high-value paths

- `/catalog/flagship-widget` returns `<meta content="nosnippet" name="googlebot">`.
  The `content` attribute appears before `name` in source order, and the meta
  name is the Google-specific `googlebot` form rather than the general
  `robots` form — both are equally valid and this extraction reads the tag's
  attributes independently of order and of which of the two names is used.

## AI crawler implications

- `nosnippet` prevents Google from showing a text snippet for this page.
  Because snippet eligibility is required for a supporting link in Google AI
  Overviews and AI Mode, this is a critical AI-feature exclusion whether it
  was declared via `name="robots"` or `name="googlebot"`.
- This directive also affects classic Google Search result previews for this
  page, not just AI features.

## Recommended robots.txt changes

No `robots.txt` change applies here since `robots.txt` does not cause this
exclusion - `robots.txt` already reflects the intended permissive policy:

```
User-agent: *
Allow: /
```

Removing the `nosnippet` directive from the page's `<meta name="googlebot">`
tag would restore snippet eligibility for both classic Search and AI
features. Confirm this is the intended content policy before recommending
removal — some publishers set this deliberately to withhold pricing or
review text from any snippet while remaining indexed.

## Verification commands

```bash
curl -s https://example.com/catalog/flagship-widget | grep -oiE '<meta[^>]+googlebot[^>]*>'
curl -sI https://example.com/catalog/flagship-widget | grep -i x-robots-tag
```

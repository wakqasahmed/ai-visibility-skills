## Current crawler policy summary

- The default `User-agent: *` stanza has no `Disallow`, so unnamed crawlers can
  fetch the site.
- `User-agent: GPTBot` has `Allow: /`, permitting OpenAI's training crawler.
- `User-agent: OAI-SearchBot` has `Disallow: /`, blocking OpenAI's search crawler
  from the entire site.

## Blocked high-value paths

- Every public path is blocked for OAI-SearchBot: `robots.txt` places
  `Disallow: /` under `User-agent: OAI-SearchBot`.

## AI crawler implications

- OAI-SearchBot is OpenAI's citation-path crawler, so this rule prevents it from
  indexing public pages for ChatGPT search results. Allowing GPTBot does not
  offset this block because GPTBot is the separate training crawler.
- Removing the block permits crawling but does not guarantee that ChatGPT will
  index or cite any page.

## Recommended robots.txt changes

Replace the OAI-SearchBot block with an explicit allow while preserving the
separate GPTBot policy:

```
User-agent: OAI-SearchBot
Allow: /
```

## Verification commands

```bash
curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
curl -s -o /dev/null -w "%{http_code}\n" -A "OAI-SearchBot" https://example.com/
```

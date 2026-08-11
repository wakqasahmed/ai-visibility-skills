## Current crawler policy summary

- Default `User-agent: *` has no `Disallow` - all other crawlers, including search
  engines, can fetch the whole site.
- A dedicated `User-agent: GPTBot` stanza carries `Disallow: /`, blocking GPTBot
  from the entire site.
- `Sitemap: https://example.com/sitemap.xml` is declared and reachable.

## Blocked high-value paths

- Entire site is blocked for GPTBot: `robots.txt` has `Disallow: /` under
  `User-agent: GPTBot`, confirmed live - `curl -A "GPTBot" .../products/widget`
  returned `403`, while the same URL returned `200` for a default user-agent.

## AI crawler implications

- GPTBot (OpenAI's training/browsing crawler) cannot read any page, including
  product pages, so this site cannot be cited or summarized by ChatGPT's web
  browsing or training corpus while this rule stands.
- No stanza was found for other named AI crawlers (ClaudeBot, PerplexityBot,
  Google-Extended), so they fall under the permissive `User-agent: *` rule and
  are not blocked.

## Recommended robots.txt changes

Remove the GPTBot-specific block so it falls back to the permissive default,
or replace it with an explicit allow:

```
User-agent: GPTBot
Allow: /
```

This improves the odds that ChatGPT can browse and cite this site's public
pages - it does not guarantee inclusion or citation, since OpenAI's crawling
and citation behavior is independent of any single robots.txt change.

## Verification commands

```bash
curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://example.com/products/widget
# expect: 200 (was: 403)
curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
```

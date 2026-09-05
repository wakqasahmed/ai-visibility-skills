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

- GPTBot is OpenAI's training crawler, so it cannot collect any page for model
  training while this rule stands. This rule does not block the separately
  controlled OAI-SearchBot citation path or ChatGPT-User fetcher.
- No stanza was found for other named AI crawlers, so they fall under the
  permissive `User-agent: *` rule and are not blocked.

## Recommended robots.txt changes

Remove the GPTBot-specific block so it falls back to the permissive default,
or replace it with an explicit allow:

```
User-agent: GPTBot
Allow: /
```

This permits OpenAI's training crawler to fetch public pages. It does not
guarantee any platform outcome and does not change the separate OAI-SearchBot
or ChatGPT-User policies.

## Verification commands

```bash
curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://example.com/products/widget
# expect: 200 (was: 403)
curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
```

## Current crawler policy summary

- A single default `User-agent: *` stanza with no `Disallow` and a
  `Crawl-delay: 20` applies to every crawler, named or not.
- No dedicated stanzas exist for PerplexityBot, Google-Extended, GPTBot,
  ClaudeBot, CCBot, Bytespider, or Amazonbot - they all inherit the default
  rule.
- `Sitemap` is declared.

## Blocked high-value paths

No paths are currently blocked for PerplexityBot, which returns `200` on the
homepage. The default `User-agent: *` policy also does not block the
`Google-Extended` robots-only control token; it has no HTTP user-agent to test.

## AI crawler implications

- PerplexityBot can currently fetch this site, but the 20-second `Crawl-delay`
  applies to it and may slow discovery of new or updated pages.
- Google-Extended is not a browsing or citation crawler. Its inherited
  `robots.txt` policy currently permits Google's training and grounding uses.
- Because there are no explicit per-bot stanzas, any future decision to
  block or throttle a specific bot (e.g. a scraper-heavy one like Bytespider)
  cannot be made without also affecting every other crawler under the same
  default rule.

## Recommended robots.txt changes

Add explicit stanzas for the AI crawlers you want to encourage, without a
crawl delay, and keep (or raise) the delay only for bots you are less
interested in:

```
User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: *
Crawl-delay: 20
Disallow:
```

Tradeoffs to weigh before applying this: removing crawl delay for these bots
increases how often they can fetch pages, which raises bandwidth/hosting
cost and re-exposes any scraping-style reuse of your content in their
outputs; keeping the current blanket delay protects cost and control but
slows how quickly new content becomes citable. This change improves the
odds these platforms crawl and cite the site promptly - it does not
guarantee they will choose to include or cite it.

## Verification commands

```bash
curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
curl -s -o /dev/null -w "%{http_code}\n" -A "PerplexityBot" https://example.com/
```

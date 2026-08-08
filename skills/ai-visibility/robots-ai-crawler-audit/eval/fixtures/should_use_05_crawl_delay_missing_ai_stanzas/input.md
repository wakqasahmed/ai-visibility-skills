# Request

We want AI tools like Perplexity and Google's AI Overviews to be able to cite our
site, but we're also worried about scraping and bandwidth costs. What does our
current robots.txt do, and what should we change?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Crawl-delay: 20
Disallow:

Sitemap: https://example.com/sitemap.xml
```

## Per-bot rule extraction

```
$ curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
User-agent: * | Disallow:
```

No stanzas found for PerplexityBot, Google-Extended, GPTBot, ClaudeBot, CCBot,
Bytespider, or Amazonbot - all fall under the default rule with a 20-second
crawl delay.

## Live fetch check

```
$ curl -s -o /dev/null -w "%{http_code}\n" -A "PerplexityBot" https://example.com/
200
$ curl -s -o /dev/null -w "%{http_code}\n" -A "Google-Extended" https://example.com/
200
```

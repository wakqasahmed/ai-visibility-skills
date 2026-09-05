# Request

We checked robots.txt and it doesn't block OAI-SearchBot at all, but pages
still don't seem to get crawled for ChatGPT search. What's going on?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

## Per-bot rule extraction

```
$ curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
User-agent: * | Disallow:
```

No explicit OAI-SearchBot stanza found.

## Live fetch as each bot

```
$ curl -s -o /dev/null -w "%{http_code}\n" \
    -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot' \
    https://example.com/blog/post-1
403
$ curl -s -o /dev/null -w "%{http_code}\n" \
    -A 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)' \
    https://example.com/blog/post-1
200
$ curl -s -o /dev/null -w "%{http_code}\n" https://example.com/blog/post-1
200
```

# Request

We checked robots.txt and it doesn't block ClaudeBot at all, but Claude still can't
seem to browse our site. What's going on?

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

No explicit ClaudeBot stanza found.

## Live fetch as each bot

```
$ curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://example.com/blog/post-1
200
$ curl -s -o /dev/null -w "%{http_code}\n" -A "ClaudeBot" https://example.com/blog/post-1
403
$ curl -s -o /dev/null -w "%{http_code}\n" https://example.com/blog/post-1
200
```

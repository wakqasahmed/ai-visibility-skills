# Request

Our ChatGPT plugin team says GPTBot never seems to fetch our pages. Can you check our
crawler access rules and tell us why?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

User-agent: GPTBot
Disallow: /

Sitemap: https://example.com/sitemap.xml
```

## Live fetch check

```
$ curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://example.com/products/widget
403
$ curl -s -o /dev/null -w "%{http_code}\n" https://example.com/products/widget
200
```

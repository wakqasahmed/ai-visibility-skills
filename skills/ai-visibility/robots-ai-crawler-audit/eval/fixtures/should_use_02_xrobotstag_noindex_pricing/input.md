# Request

AI search tools never mention our pricing page even though robots.txt looks fine.
Can you dig into why?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow: /internal/

Sitemap: https://example.com/sitemap.xml
```

## Header check on the pricing page

```
$ curl -sI https://example.com/pricing | grep -i x-robots-tag
X-Robots-Tag: noindex, nofollow
```

## Meta tag check on the same page

```
$ curl -s https://example.com/pricing | grep -oiE '<meta[^>]+robots[^>]+>'
(no output - no meta robots tag present)
```

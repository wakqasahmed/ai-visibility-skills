# Request

Our docs pages used to show up in AI answers and now they don't. Nothing changed in
robots.txt as far as we know. Can you check?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

## Header check on /docs/getting-started

```
$ curl -sI https://example.com/docs/getting-started | grep -i x-robots-tag
(no output)
```

## Meta tag check on the same page

```
$ curl -s https://example.com/docs/getting-started | grep -oiE '<meta[^>]+robots[^>]+>'
<meta name="robots" content="noindex, nofollow">
```

## Canonical tag check

```
$ curl -s https://example.com/docs/getting-started | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
<link rel="canonical" href="https://example.com/docs/getting-started">
```

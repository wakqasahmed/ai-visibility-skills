# Request

Our robots.txt and meta robots tags look clean on shoreline-goods.example, but a
security scanner flagged some missing response headers on our product pages. Can
you check whether that's worth fixing as part of this audit?

## robots.txt (fetched from https://shoreline-goods.example/robots.txt)

```
User-agent: *
Disallow: /account/
Disallow: /checkout/

Sitemap: https://shoreline-goods.example/sitemap.xml
```

## Header check on a product page

```
$ curl -sI https://shoreline-goods.example/products/tide-lantern
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: nginx

$ curl -sI https://shoreline-goods.example/products/tide-lantern | grep -i "strict-transport-security"
(no output)
$ curl -sI https://shoreline-goods.example/products/tide-lantern | grep -i "x-content-type-options"
(no output)
$ curl -sI https://shoreline-goods.example/products/tide-lantern | grep -i "x-frame-options"
(no output)
```

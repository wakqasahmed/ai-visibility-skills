# Request

Can crawlers find our pages? Our site is `https://tidewater-studio.example` (Gatsby, deployed to
an S3 website endpoint behind CloudFront). Someone told us we have no sitemap at all, which
doesn't sound right — the build definitely generates one.

What we know:

```
$ curl -s -o /dev/null -w "%{http_code}\n" https://tidewater-studio.example/sitemap.xml
404
$ curl -s -o /dev/null -w "%{http_code}\n" https://tidewater-studio.example/sitemap_index.xml
404
$ curl -s https://tidewater-studio.example/robots.txt
User-agent: *
Allow: /
```

Homepage `<head>` includes:

```html
<link rel="sitemap" type="application/xml" href="/sitemap-index.xml">
```

Canonical on the homepage is `<link rel="canonical" href="https://tidewater-studio.example/">`.
Apex serves fine over HTTPS. We've never checked whether `www.tidewater-studio.example` works.

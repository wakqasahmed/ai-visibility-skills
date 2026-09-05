# Request

We only have a `<meta name="robots">` on some pages, but our CMS templating
puts the `content` attribute before `name` on this one, and one product page
uses the Google-specific `googlebot` meta name instead of `robots`. Does that
still count?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

## Header check on /catalog/flagship-widget

```
$ curl -sI https://example.com/catalog/flagship-widget | grep -i x-robots-tag
(no output)
```

## HTML from the same page

```html
<!doctype html>
<html lang="en">
<head>
  <title>Flagship Widget</title>
  <meta content="nosnippet" name="googlebot">
  <link rel="canonical" href="https://example.com/catalog/flagship-widget">
</head>
<body>
  <main><h1>Flagship Widget</h1><p>Product details...</p></main>
</body>
</html>
```

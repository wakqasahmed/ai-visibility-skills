# Request

A developer added `data-nosnippet` to a `<p>` tag on our pricing page hoping
it would hide the price from AI Overviews. Did it work?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

## Header check on /pricing

```
$ curl -sI https://example.com/pricing | grep -i x-robots-tag
(no output)
```

## HTML from the same page

```html
<!doctype html>
<html lang="en">
<head>
  <title>Pricing</title>
  <link rel="canonical" href="https://example.com/pricing">
</head>
<body>
  <main>
    <h1>Pricing</h1>
    <p data-nosnippet>Starting at $49/month, billed annually.</p>
  </main>
</body>
</html>
```

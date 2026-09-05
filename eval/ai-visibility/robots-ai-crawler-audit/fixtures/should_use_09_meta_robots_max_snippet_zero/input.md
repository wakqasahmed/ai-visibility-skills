# Request

Our research page is indexed in Google, but we want it to appear in AI Overviews and
AI Mode. Can you check whether our crawler controls interfere with that goal?

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

## Header check on /research/market-report

```
$ curl -sI https://example.com/research/market-report | grep -i x-robots-tag
(no output)
```

## HTML from the same page

```html
<!doctype html>
<html lang="en">
<head>
  <title>2026 Market Report</title>
  <meta name="robots" content="max-snippet:0">
  <link rel="canonical" href="https://example.com/research/market-report">
</head>
<body>
  <main><h1>2026 Market Report</h1><p>Research findings...</p></main>
</body>
</html>
```

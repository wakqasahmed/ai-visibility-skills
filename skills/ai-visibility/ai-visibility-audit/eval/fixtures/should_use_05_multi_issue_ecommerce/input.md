Full AI visibility audit please, we're about to run a big ad campaign and want AI shopping agents to be able to find and recommend us. Site: https://cascadekettles.example

`robots.txt`:

```
User-agent: CCBot
Disallow: /

User-agent: *
Disallow: /cart/
Sitemap: https://cascadekettles.example/sitemap.xml
```

Representative product page (`https://cascadekettles.example/products/copper-kettle`), fetched normally:

```html
<!doctype html>
<html lang="en">
<head>
  <title>Copper Kettle - Cascade Kettles</title>
  <meta name="description" content="Hand-hammered copper kettle, 1.5L, made in Oregon.">
  <link rel="canonical" href="https://cascadekettles.example/products/copper-kettle">
</head>
<body>
  <h1>Hand-Hammered Copper Kettle</h1>
  <p>1.5L capacity, made in Oregon, stovetop and induction safe.</p>
</body>
</html>
```

No `<script type="application/ld+json">` Product schema anywhere on the site. FAQ page has one question ("What's your return policy?") answered with "See our policy page." with no link or detail.

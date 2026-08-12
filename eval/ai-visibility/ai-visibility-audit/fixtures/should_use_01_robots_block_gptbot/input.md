Can you check if my site is visible to AI tools like ChatGPT and Claude? Site: https://boulderworks.example

`robots.txt`:

```
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: *
Disallow: /checkout/
Sitemap: https://boulderworks.example/sitemap.xml
```

Representative page (`https://boulderworks.example/`), fetched normally:

```html
<!doctype html>
<html lang="en">
<head>
  <title>Boulderworks - Custom Climbing Holds</title>
  <meta name="description" content="Boulderworks makes custom climbing holds for home and commercial gyms.">
  <link rel="canonical" href="https://boulderworks.example/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Boulderworks"}</script>
</head>
<body>
  <h1>Custom Climbing Holds, Made in the US</h1>
  <p>Boulderworks has manufactured resin climbing holds since 2015, tested for grip and durability.</p>
</body>
</html>
```

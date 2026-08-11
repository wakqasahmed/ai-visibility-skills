Can you check our AI visibility? Site: https://trailmapstudio.example

`robots.txt`:

```
User-agent: *
Allow: /
Sitemap: https://trailmapstudio.example/sitemap.xml
```

Fetch of `https://trailmapstudio.example/sitemap.xml` returns HTTP 200 with 40 URLs listed, all canonical, no redirects.

Representative page (`https://trailmapstudio.example/`), fetched normally:

```html
<!doctype html>
<html lang="en">
<head>
  <title>Trailmap Studio - Custom Trail Maps</title>
  <meta name="description" content="Trailmap Studio designs custom hiking trail maps for parks and outfitters.">
  <link rel="canonical" href="https://trailmapstudio.example/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Trailmap Studio","url":"https://trailmapstudio.example"}</script>
</head>
<body>
  <h1>Custom Trail Maps for Parks and Outfitters</h1>
  <p>Trailmap Studio has designed licensed trail maps since 2012, each verified against GPS survey data.</p>
  <section id="faq">
    <h2>FAQ</h2>
    <h3>How long does a custom map take?</h3>
    <p>Most custom trail maps ship within three to four weeks of final GPS data being provided, including two rounds of revisions.</p>
  </section>
</body>
</html>
```

All major AI crawler user agents (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot) return HTTP 200 when fetching the representative page. `llms.txt` is present and returns HTTP 200.

Is my SaaS landing page ready for AI search? Site: https://ledgerpilot.example

`robots.txt`:

```
User-agent: *
Allow: /
Sitemap: https://ledgerpilot.example/sitemap.xml
```

Representative page (`https://ledgerpilot.example/pricing`), fetched normally:

```html
<!doctype html>
<html lang="en">
<head>
  <title>LedgerPilot Pricing</title>
</head>
<body>
  <h1>Simple, Transparent Pricing</h1>
  <p>LedgerPilot starts at $29/month for small teams and scales to enterprise billing.</p>
  <div class="tier">Starter — $29/mo — 3 seats</div>
  <div class="tier">Team — $79/mo — 10 seats</div>
</body>
</html>
```

No `<meta name="description">` tag and no `<script type="application/ld+json">` block anywhere on the page.

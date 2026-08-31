Is `https://harborline.example` ready for AI search? It's a Gatsby site whose marketing pages are
rendered with React Helmet, and the pricing page is served by a Next.js App Router app.

Homepage, raw response (`curl -s https://harborline.example`), `<head>` excerpt:

```html
<head>
  <meta charset="utf-8">
  <title data-react-helmet="true">Harborline — Fleet Maintenance Software</title>
  <meta data-react-helmet="true" name="description" content="Harborline schedules preventive maintenance for commercial marine fleets.">
  <link data-react-helmet="true" rel="canonical" href="https://harborline.example/">
</head>
```

Pricing page (`https://harborline.example/pricing`), raw response: no
`<script ... application/ld+json>` match; the body is 190 `self.__next_f.push([1,"..."])` chunks.

Same pricing page rendered headless (`chrome --headless=new --dump-dom`): 2 JSON-LD blocks,
`Organization` and `BreadcrumbList`, both well-formed.

`robots.txt` allows all crawlers and declares the sitemap.

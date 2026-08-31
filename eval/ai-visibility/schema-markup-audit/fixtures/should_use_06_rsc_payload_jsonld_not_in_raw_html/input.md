Audit the structured data on our homepage `https://northwind-labs.example`. It's a Next.js App
Router site.

Raw HTML pass:

```bash
$ curl -s "https://northwind-labs.example" | grep -oiE '<script[^>]+application/ld\+json[^>]*>[^<]*'
$ curl -s "https://northwind-labs.example" | grep -c '__next_f'
214
```

Zero JSON-LD blocks matched. The response body is mostly `self.__next_f.push([1,"..."])` chunks.

Hydrated pass (headless Chromium `--dump-dom`):

```bash
$ chrome --headless=new --dump-dom "https://northwind-labs.example" > /tmp/hydrated.html
$ grep -oiE '<script[^>]+application/ld\+json[^>]*>' /tmp/hydrated.html | wc -l
4
```

The four blocks in the hydrated DOM are `BreadcrumbList` (×2), `FAQPage` (7 Q&A pairs matching
the visible FAQ section verbatim), and an `Organization` block injected with
`dangerouslySetInnerHTML` under `id="homepage-jsonld"`:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Northwind Labs",
  "url": "https://northwind-labs.example"
}
```

Visible on the page: the company name "Northwind Labs", a logo at
`https://northwind-labs.example/logo.svg`, and footer links to the company's LinkedIn
(`https://www.linkedin.com/company/northwind-labs`) and GitHub
(`https://github.com/northwind-labs`) profiles.

Do we have structured data or not, and what should we fix?

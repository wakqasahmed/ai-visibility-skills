# Request

Draft an llms.txt for our SaaS product site so AI agents understand what we do and where the docs are.

## Crawl results

```
curl -s -o /dev/null -w "%{http_code}\n" "https://acmeflow.dev/llms.txt"
404
```

```
curl -s "https://acmeflow.dev" | grep -oE '<title>[^<]*'
<title>AcmeFlow — workflow automation for small teams
curl -s "https://acmeflow.dev" | grep -oE '<meta name="description"[^>]*>'
<meta name="description" content="AcmeFlow automates repetitive team workflows with no-code triggers and integrations.">
```

```
curl -s "https://acmeflow.dev/sitemap.xml" | grep -oE '<loc>[^<]+</loc>'
<loc>https://acmeflow.dev/</loc>
<loc>https://acmeflow.dev/docs</loc>
<loc>https://acmeflow.dev/docs/quickstart</loc>
<loc>https://acmeflow.dev/pricing</loc>
<loc>https://acmeflow.dev/integrations</loc>
<loc>https://acmeflow.dev/support</loc>
<loc>https://acmeflow.dev/privacy</loc>
<loc>https://acmeflow.dev/terms</loc>
```

All eight URLs above return HTTP 200 (spot-checked individually).

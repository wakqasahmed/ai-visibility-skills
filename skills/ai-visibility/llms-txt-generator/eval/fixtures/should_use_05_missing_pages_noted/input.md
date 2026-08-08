# Request

Draft an llms.txt for our API product.

## Crawl results

```
curl -s -o /dev/null -w "%{http_code}\n" "https://queuelayer.dev/llms.txt"
404
```

```
curl -s "https://queuelayer.dev/sitemap.xml" | grep -oE '<loc>[^<]+</loc>'
<loc>https://queuelayer.dev/</loc>
<loc>https://queuelayer.dev/docs</loc>
<loc>https://queuelayer.dev/status</loc>
```

All 3 URLs confirmed HTTP 200. The homepage links to "/pricing" in its nav, but:

```
curl -s -o /dev/null -w "%{http_code}\n" "https://queuelayer.dev/pricing"
404
```

`/pricing` 404s and is not in the sitemap — it looks like the page was never actually published, only linked from the nav.

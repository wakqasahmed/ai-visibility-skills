# Request

We're an online retailer. Please draft an llms.txt so AI shopping assistants understand what we sell and where our policies live.

## Crawl results

```
curl -s -o /dev/null -w "%{http_code}\n" "https://brightleaf.store/llms.txt"
404
```

```
curl -s "https://brightleaf.store" | grep -oE '<title>[^<]*'
<title>Brightleaf — sustainable home goods
```

```
curl -s "https://brightleaf.store/sitemap.xml" | grep -oE '<loc>[^<]+</loc>'
<loc>https://brightleaf.store/</loc>
<loc>https://brightleaf.store/collections/kitchen</loc>
<loc>https://brightleaf.store/collections/bedding</loc>
<loc>https://brightleaf.store/shipping-policy</loc>
<loc>https://brightleaf.store/returns-policy</loc>
<loc>https://brightleaf.store/support</loc>
<loc>https://brightleaf.store/about</loc>
<loc>https://brightleaf.store/contact</loc>
```

All 8 URLs confirmed HTTP 200 individually.

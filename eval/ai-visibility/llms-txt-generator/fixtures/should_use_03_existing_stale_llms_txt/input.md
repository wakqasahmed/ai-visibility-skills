# Request

Our llms.txt is a year old, review and update it — a couple of links might be dead.

## Crawl results

```
curl -s -o /dev/null -w "%{http_code}\n" "https://harborcloud.io/llms.txt"
200
curl -s "https://harborcloud.io/llms.txt"
# HarborCloud

HarborCloud is managed Postgres hosting.

## Docs

- [Docs](https://harborcloud.io/docs): Product documentation.
- [Legacy API v1](https://harborcloud.io/docs/api-v1): Old API reference.
```

```
curl -s -o /dev/null -w "%{http_code}\n" "https://harborcloud.io/docs/api-v1"
404
curl -s -o /dev/null -w "%{http_code}\n" "https://harborcloud.io/docs"
200
```

```
curl -s "https://harborcloud.io/sitemap.xml" | grep -oE '<loc>[^<]+</loc>'
<loc>https://harborcloud.io/</loc>
<loc>https://harborcloud.io/docs</loc>
<loc>https://harborcloud.io/docs/api-v2</loc>
<loc>https://harborcloud.io/pricing</loc>
<loc>https://harborcloud.io/status</loc>
```

`/docs/api-v2` and `/pricing` and `/status` all return HTTP 200 (spot-checked). `/docs/api-v1` returns 404 — it was replaced by `/docs/api-v2`.

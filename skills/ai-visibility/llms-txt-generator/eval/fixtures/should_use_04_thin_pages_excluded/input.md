# Request

Draft an llms.txt for our blog/publishing site.

## Crawl results

```
curl -s -o /dev/null -w "%{http_code}\n" "https://fieldnote.blog/llms.txt"
404
```

```
curl -s "https://fieldnote.blog/sitemap.xml" | grep -oE '<loc>[^<]+</loc>'
<loc>https://fieldnote.blog/</loc>
<loc>https://fieldnote.blog/archive</loc>
<loc>https://fieldnote.blog/about</loc>
<loc>https://fieldnote.blog/tag/gardening</loc>
<loc>https://fieldnote.blog/tag/travel</loc>
<loc>https://fieldnote.blog/tag/food</loc>
<loc>https://fieldnote.blog/archive?print=1</loc>
<loc>https://fieldnote.blog/archive?print=1&lang=en</loc>
```

All 8 URLs return HTTP 200. The `/tag/*` pages are auto-generated tag-archive listings with no unique body copy beyond a repeated post-title list. `/archive?print=1` and `/archive?print=1&lang=en` are print-friendly duplicates of `/archive` with identical content.

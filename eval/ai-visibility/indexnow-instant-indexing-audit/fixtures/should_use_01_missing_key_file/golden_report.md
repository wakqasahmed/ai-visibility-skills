# IndexNow Audit Report: example.com

## IndexNow Key Verification Status
- Host: `example.com`
- Key location: `https://example.com/a1b2c3d4e5f6.txt`
- Result: **MISSING** (HTTP 404 returned when checking `https://example.com/a1b2c3d4e5f6.txt`).
- Manifest: No `/indexnow.json` found.

## Submission Endpoint & Payload Configuration
- API target: `https://api.indexnow.org/indexnow`
- Sample payload evaluated:
```json
{
  "host": "example.com",
  "key": "a1b2c3d4e5f6",
  "keyLocation": "https://example.com/a1b2c3d4e5f6.txt",
  "urlList": ["https://example.com/blog/article-1"]
}
```
- Status: Submission rejected by `api.indexnow.org` due to unverified host key.

## CMS & Webhook Push Integration
- CMS: Next.js App Router.
- Webhook trigger: Absent. New articles rely exclusively on Googlebot and Bingbot polling the XML sitemap.

## Recommended Fixes & Implementation
1. Generate an 8+ character hex key string: `a1b2c3d4e5f6`.
2. Host the key at the domain root: `public/a1b2c3d4e5f6.txt` containing `a1b2c3d4e5f6`.
3. Add a Next.js revalidation webhook to POST updated URLs to `https://api.indexnow.org/indexnow`.

## Verification Commands
```bash
# Verify key file returns 200
curl -s -i "https://example.com/a1b2c3d4e5f6.txt"

# Test submission endpoint
curl -s -X POST "https://api.indexnow.org/indexnow"      -H "Content-Type: application/json; charset=utf-8"      -d '{"host":"example.com","key":"a1b2c3d4e5f6","urlList":["https://example.com/blog/article-1"]}'
```

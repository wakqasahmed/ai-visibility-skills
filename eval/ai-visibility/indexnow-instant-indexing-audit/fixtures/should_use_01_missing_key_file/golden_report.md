# IndexNow Audit Report: example.com

## IndexNow Key Verification Status
- Host: `example.com`
- Key-hosting mechanism: root `{key}.txt` (no `keyLocation` configured).
- Expected key file: `https://example.com/a1b2c3d4e5f6.txt`
- Observed: **MISSING** — HTTP 404 returned for the key file.
- Key charset/length: `a1b2c3d4e5f6` is 12 characters and matches `^[A-Za-z0-9-]{8,128}$`, so the key
  string itself conforms; only its hosting is absent.

## Submission Endpoint & Payload Configuration
- Endpoint the CMS is configured to call: `https://api.indexnow.org/indexnow`
- Configured payload, validated statically (no live submission performed):
```json
{
  "host": "example.com",
  "key": "a1b2c3d4e5f6",
  "urlList": ["https://example.com/blog/article-1"]
}
```
- `keyLocation` path scoping: not applicable — no `keyLocation` is set, so the key is expected at the
  host root and every root-level path in `urlList` is in scope once the file exists.
- Expected response code: HTTP 403 (key validation failed — key file not found), because the key file
  returns HTTP 404. This is the code the current configuration will produce; a live submission was
  withheld pending operator authorization, so it is not an observed submission result.

## CMS & Webhook Push Integration
- CMS: Next.js App Router.
- Push trigger: **MISSING**. New articles rely exclusively on Bingbot polling the XML sitemap.

## Recommended Fixes & Implementation
1. Generate a key of 8-128 characters using only `a-z`, `A-Z`, `0-9`, or `-`, e.g. `a1b2c3d4e5f6`.
2. Host it at the site root as `public/a1b2c3d4e5f6.txt`, served with `Content-Type: text/plain` and a
   body that is exactly `a1b2c3d4e5f6`.
3. Re-run the key-file check below and confirm HTTP 200 before enabling any push.
4. Add a Next.js revalidation hook that POSTs published and updated URLs to
   `https://api.indexnow.org/indexnow`, excluding drafts and preview URLs.

## Verification Commands
```bash
# Read-only: verify the key file returns 200 text/plain with the key as its body.
curl -s -i "https://example.com/a1b2c3d4e5f6.txt"
```

A live POST to `https://api.indexnow.org/indexnow` enters URLs into Bing's and Yandex's indexing
queues; it is a state-changing submission, not an inspection. It is therefore not run as part of this
audit. Request it explicitly once the operator confirms control of `example.com` and the key file
returns HTTP 200.

# IndexNow Audit Report: news.example.com

## IndexNow Key Verification Status
- Host: `news.example.com`
- Key-hosting mechanism: root `{key}.txt` at `https://news.example.com/newskey789.txt`
- Observed: **COMPLIANT** — HTTP 200 with `Content-Type: text/plain` and a body equal to
  `newskey789`.
- Key charset/length: 10 characters, matches `^[A-Za-z0-9-]{8,128}$` — conforming.

## Submission Endpoint & Payload Configuration
- Endpoint configured in the plugin: `https://yandex.com/indexnow`
- Payload fields: `host`, `key`, `urlList`. `keyLocation` omitted, correct for a root key file.
- `keyLocation` path scoping: not applicable — root key file authorizes the whole host.
- **PARTIAL** — the payload is well-formed and would return HTTP 200 if sent, but no submission has
  been made in the audited period, so no response code has been observed. Nothing was submitted
  during this audit; a live push requires operator authorization.

## CMS & Webhook Push Integration
- Platform: WordPress.
- Push trigger: **MISSING**. The IndexNow plugin is installed but deactivated, so `publish_post` and
  `post_updated` never fire a submission. This is the reason new articles are only discovered when
  Bingbot next polls the sitemap, despite the key file being valid.

## Recommended Fixes & Implementation
1. Activate the official Microsoft IndexNow plugin for WordPress.
2. Enable automatic push on post publish and post update, and include deletions and 301 redirects.
3. Exclude drafts, scheduled posts, and preview URLs from push batches.
4. Log the response code of each push so an HTTP 403 or HTTP 422 surfaces instead of failing silently.

## Verification Commands
```bash
# Read-only: confirm the key file returns 200 text/plain with the exact key as its body.
curl -s -i "https://news.example.com/newskey789.txt"
```

# IndexNow Audit Report: example.com

## IndexNow Key Verification Status
- Key file `https://example.com/a1b2c3d4e5f6.txt` returned HTTP 404 — **MISSING**.

## Submission Endpoint & Payload Configuration
- Endpoint: `https://api.indexnow.org/indexnow` with `host`, `key`, `urlList`.
- Expected response code: HTTP 403 (key validation failed).

## CMS & Webhook Push Integration
- No publish-time push trigger is configured.

## Recommended Fixes & Implementation
1. Host the key file at the root and enable the publish hook.
2. Once this is in place, IndexNow guarantees Bing indexes every new article within an hour.

## Verification Commands
```bash
curl -s -i "https://example.com/a1b2c3d4e5f6.txt"
```

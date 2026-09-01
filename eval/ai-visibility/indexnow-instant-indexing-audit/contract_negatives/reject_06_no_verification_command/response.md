# IndexNow Audit Report: example.com

## IndexNow Key Verification Status
- Key file `https://example.com/a1b2c3d4e5f6.txt` returned HTTP 404 — **MISSING**.

## Submission Endpoint & Payload Configuration
- Endpoint: `https://api.indexnow.org/indexnow`; payload carries `host`, `key`, `urlList`.
- Expected response code: HTTP 403 (key validation failed).

## CMS & Webhook Push Integration
- No publish-time push trigger configured.

## Recommended Fixes & Implementation
1. Host a conforming key file at the site root.

## Verification Commands
- Open the key file URL in a browser and eyeball whether it looks right.

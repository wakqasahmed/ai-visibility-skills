# IndexNow Audit Report: shop.example.com

## IndexNow Key Verification Status
- Host: `shop.example.com`
- Key location: `https://shop.example.com/key12345.txt`
- Result: **MALFORMED** (HTTP 200 returned, but body contained HTML error page rather than the exact key string `key12345`).

## Submission Endpoint & Payload Configuration
- Endpoint: `https://www.bing.com/indexnow`
- Payload validation: Key header did not match content of key file.

## CMS & Webhook Push Integration
- Platform: WordPress with WooCommerce.
- Plugin: Custom theme redirect intercepting `.txt` URLs.

## Recommended Fixes & Implementation
1. Exclude `/*.txt` paths from WordPress `.htaccess` / Nginx rewrite rules.
2. Ensure `/key12345.txt` returns raw text `key12345` with `Content-Type: text/plain`.

## Verification Commands
```bash
curl -s "https://shop.example.com/key12345.txt"
```

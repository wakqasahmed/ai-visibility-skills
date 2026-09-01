# IndexNow Audit Report: shop.example.com

## IndexNow Key Verification Status
- Host: `shop.example.com`
- Key-hosting mechanism: root `{key}.txt` at `https://shop.example.com/key12345.txt`
- Observed: **MALFORMED** — HTTP 200 returned, but the response body is a WordPress HTML error page,
  not the exact key string `key12345`. `Content-Type` observed as `text/html; charset=UTF-8`;
  the spec requires a UTF-8 text file, so `text/plain` is expected.
- Key charset/length: `key12345` is 8 characters and matches `^[A-Za-z0-9-]{8,128}$` — conforming.

## Submission Endpoint & Payload Configuration
- Endpoint: `https://www.bing.com/indexnow`
- Payload fields present: `host`, `key`, `urlList`. No `keyLocation`, which is correct for a root key
  file, so path scoping is not applicable and every `urlList` path is in scope.
- Expected response code: HTTP 403 (key validation failed). The key travels in the JSON `key` field
  (or the GET query string) and is verified against the *contents* of the hosted key file; because the
  file's body does not equal `key12345`, verification fails. IndexNow defines no key HTTP header, so
  there is no header mismatch to report here.

## CMS & Webhook Push Integration
- Platform: WordPress with WooCommerce.
- Push trigger: present via the IndexNow plugin, but every push fails key verification, so no URL is
  actually accepted.
- Root cause: a custom theme rewrite intercepts `.txt` requests and returns a themed error page with a
  200 status.

## Recommended Fixes & Implementation
1. Exclude `/*.txt` paths from the WordPress `.htaccess` / Nginx rewrite rules so the static file is
   served directly.
2. Ensure `https://shop.example.com/key12345.txt` returns raw text `key12345` with
   `Content-Type: text/plain` and no HTML wrapper or trailing markup.
3. Re-run the check below and confirm the body equals the key exactly before re-enabling pushes.

## Verification Commands
```bash
# Read-only: assert the key file's status, content type, and exact body.
curl -s -i "https://shop.example.com/key12345.txt"
```

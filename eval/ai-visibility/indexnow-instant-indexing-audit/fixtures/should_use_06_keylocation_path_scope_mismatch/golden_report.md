# IndexNow Audit Report: example.com

## IndexNow Key Verification Status
- Host: `example.com`
- Key-hosting mechanism: non-root key file declared via `keyLocation`,
  `https://example.com/static/keys/b7c2d91f4a8e.txt`
- Observed: **COMPLIANT in isolation** — HTTP 200 with `Content-Type: text/plain` and a body equal to
  `b7c2d91f4a8e`. The key file itself is served correctly, which is why the misconfiguration is easy
  to miss.
- Key charset/length: 12 characters, matches `^[A-Za-z0-9-]{8,128}$` — conforming.

## Submission Endpoint & Payload Configuration
- Endpoint: `https://api.indexnow.org/indexnow`
- Configured payload, validated statically (no live submission performed):
```json
{
  "host": "example.com",
  "key": "b7c2d91f4a8e",
  "keyLocation": "https://example.com/static/keys/b7c2d91f4a8e.txt",
  "urlList": [
    "https://example.com/blog/spring-release",
    "https://example.com/pricing"
  ]
}
```
- `keyLocation` path scoping: **MALFORMED**. A key file at a non-root path only authorizes URLs whose
  path starts with that same directory prefix. This key authorizes `https://example.com/static/keys/`
  only, while every URL in `urlList` sits outside that subtree.
- Expected response code: HTTP 422 (URLs do not belong to the host or violate the key's path scope).
  Note this is **not** HTTP 403: the key file resolves and its contents match, so key validation
  succeeds — the failure is authorization scope, which is exactly why every push fails silently while
  the key file still returns HTTP 200.

## CMS & Webhook Push Integration
- Push trigger: present — the publish pipeline POSTs on every content release.
- Response handling: **MISSING**. The pipeline discards the response code, so months of HTTP 422
  responses produced no alert. This is the operational defect that hid the scope violation.

## Recommended Fixes & Implementation
1. Preferred: move the key file back to the host root as
   `https://example.com/b7c2d91f4a8e.txt` and drop `keyLocation` from the payload. A root key file
   authorizes the entire host, so no path-scope check is needed.
2. Alternative, if the file must stay out of the web root: keep `keyLocation` and restrict `urlList`
   to URLs under `https://example.com/static/keys/` — which is not useful for content URLs, so
   option 1 is the practical fix.
3. Fail the publish job on any non-200/202 response, and log the code, so HTTP 403 and HTTP 422 are
   distinguished at push time.

## Verification Commands
```bash
# Read-only: confirm the non-root key file resolves with the exact key as its body.
curl -s -i "https://example.com/static/keys/b7c2d91f4a8e.txt"
```

```bash
# Read-only static check: print any urlList entry outside the keyLocation directory prefix.
python3 - <<'PY'
import json, urllib.parse
payload = json.load(open("indexnow-payload.json"))
key_loc = payload.get("keyLocation")
prefix = "/" if not key_loc else urllib.parse.urlparse(key_loc).path.rsplit("/", 1)[0] + "/"
for url in payload["urlList"]:
    path = urllib.parse.urlparse(url).path
    if not path.startswith(prefix):
        print(f"OUT OF SCOPE (would return 422): {url} not under {prefix}")
PY
```

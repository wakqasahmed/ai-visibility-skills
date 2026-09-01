# IndexNow Audit Report: docs.example.com

## IndexNow Key Verification Status
- Host: `docs.example.com`
- Key-hosting mechanism: root `{key}.txt` at `https://docs.example.com/9f8e7d6c5b4a.txt`
- Observed: **COMPLIANT** — HTTP 200 with `Content-Type: text/plain` and a body equal to
  `9f8e7d6c5b4a`.
- Key charset/length: 12 characters, matches `^[A-Za-z0-9-]{8,128}$` — conforming.

## Submission Endpoint & Payload Configuration
- Endpoint: `https://api.indexnow.org/indexnow`
- Payload fields: `host`, `key`, `urlList` (12 URLs in the most recent CI batch). `keyLocation` is
  omitted, which is correct for a root key file.
- `keyLocation` path scoping: not applicable — the key is at the host root, so the whole host is
  authorized and no `urlList` path can fall outside it.
- Most recent CI submission log records HTTP 200 (URLs submitted successfully) for the last batch.

## CMS & Webhook Push Integration
- Push trigger: GitHub Actions workflow POSTs changed documentation URLs to
  `https://api.indexnow.org/indexnow` on merge to `main`.
- Coverage: new and updated pages are pushed; deletions and 301 redirects are also included.
- Exclusions: preview deployments and draft branches are filtered out before the batch is built.

## Recommended Fixes & Implementation
- No misconfiguration found. Before scaling the batch size, keep batches within the 10,000-URL
  per-call limit and log the response code for every push so an HTTP 429 (rate-limited) or HTTP 422
  (host or path scope mismatch) is visible instead of silently discarded.
- A conforming setup improves discovery latency for participating engines; it does not by itself
  determine whether any given URL is indexed.

## Verification Commands
```bash
# Read-only: confirm the key file still returns 200 text/plain with the exact key as its body.
curl -s -i "https://docs.example.com/9f8e7d6c5b4a.txt"
```

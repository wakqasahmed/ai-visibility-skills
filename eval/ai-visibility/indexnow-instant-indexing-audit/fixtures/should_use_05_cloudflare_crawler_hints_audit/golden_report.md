# IndexNow Audit Report: app.example.com

## IndexNow Key Verification Status
- Host: `app.example.com`
- Key-hosting mechanism: **NOT APPLICABLE** — notification is delegated to the edge. With Cloudflare
  Crawler Hints enabled, Cloudflare performs the IndexNow notification itself and manages the key on
  its own side, so the origin correctly hosts no `{key}.txt` file and declares no `keyLocation`.
- No key filename is configured on the origin, so any `.txt` path under the root returns HTTP 404.
  That is the expected state for this setup, not a defect. A `{key}.txt` file on the origin would only
  be required for a custom Cloudflare Worker that POSTs to an IndexNow endpoint on the origin's
  behalf — a different setup from Crawler Hints, and not what is deployed here.

## Submission Endpoint & Payload Configuration
- Endpoint: not called by the origin. Cloudflare submits to the IndexNow endpoints from its edge when
  it observes changed content, so there is no origin-built `host`/`key`/`keyLocation`/`urlList`
  payload to validate and no response code observable from the origin.
- Consequence for the audit: submission timing and per-URL outcomes are not visible to the site owner
  here. Coverage must be confirmed in Bing Webmaster Tools rather than from an HTTP 200 on a push.

## CMS & Webhook Push Integration
- Cloudflare Crawler Hints: enabled on the zone; this is the active push mechanism.
- No CMS-side or Worker-side IndexNow integration is present, and none is needed while Crawler Hints
  is the chosen path. Running both would double-submit.

## Recommended Fixes & Implementation
1. Confirm `staging.app.example.com` and preview subdomains are on zones or hostnames with Crawler
   Hints disabled, so non-production URLs are not forwarded to IndexNow.
2. Verify discovery in Bing Webmaster Tools' URL inspection for a few recently published URLs, since
   the origin has no submission log of its own.
3. If per-URL control or submission logging is required, replace Crawler Hints with a custom Worker
   that POSTs explicit batches — that path *does* require a `{key}.txt` file reachable on the origin
   (or a declared `keyLocation`) and would then be audited as a standard key-hosting setup.

## Verification Commands
No key filename is configured anywhere on the origin or in a payload, so there is no specific
`{key}.txt` URL to probe — absence of a configured key is the finding, not a 404 on a guessed path.
What is verifiable read-only is that the zone is Cloudflare-proxied:

```bash
# Read-only: confirm requests are proxied by Cloudflare (server / cf-ray response headers present).
curl -s -I "https://app.example.com/" | grep -i -E '^(server|cf-ray):'
```

Then confirm in Bing Webmaster Tools that recently published URLs were discovered, since the origin
holds no submission log of its own.

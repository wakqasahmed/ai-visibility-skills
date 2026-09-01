---
name: indexnow-instant-indexing-audit
description: Audit whether a website implements the IndexNow protocol for instant URL discovery and indexation by Bing, Yandex, Seznam, Naver, and AI search engines.
---

# IndexNow Instant Indexing & Discovery Audit

Audit whether a website provides real-time, push-based indexation and discovery capabilities to search engines and AI answer engines via the IndexNow protocol `[INDEXNOW-SPEC-01]`, moving beyond passive pull-based sitemap polling.

## Workflow

1. **Verify IndexNow Verification Key Hosting**:
   - IndexNow defines exactly two key-hosting mechanisms `[INDEXNOW-SPEC-01]`. There is no site-hosted JSON manifest and no key HTTP header — do not probe for either.
     - A UTF-8 text file named `{key}.txt` at the host root: `https://example.com/{key}.txt`.
     - A key file at any other path on the same host, declared per-submission via the `keyLocation` field.
   - Verify the key file returns HTTP 200 with `Content-Type: text/plain` and a body that is exactly the key string (no HTML wrapper, no trailing markup).
   - Verify the key is 8-128 characters and contains only `a-z`, `A-Z`, `0-9`, or `-` `[INDEXNOW-SPEC-01]`.

2. **Audit Submission Requests & `keyLocation` Path Scoping**:
   - Batch form — POST JSON to `https://api.indexnow.org/indexnow` (or `https://www.bing.com/indexnow`, `https://yandex.com/indexnow`) `[INDEXNOW-SPEC-01]`:
     - `host`: target hostname (must match the host serving the key file).
     - `key`: the key string.
     - `keyLocation`: absolute URL of the key file when it is not at the host root.
     - `urlList`: newly published, modified, or deleted URLs (up to 10,000 per call).
   - Single-URL form — GET `https://<searchengine>/indexnow?url={url}&key={key}` (plus optional `&keyLocation={url}`).
   - **Path-scoping check** — a key file hosted at a non-root path only authorizes URLs whose path starts with that same path `[INDEXNOW-SPEC-01]`. A key at `https://example.com/catalog/{key}.txt` may submit `https://example.com/catalog/...` but not `https://example.com/help/...`. Compare the `keyLocation` directory prefix against every path in `urlList`; a mismatch means every push silently fails with `422` while the key file itself still returns 200.

3. **Audit CMS & Webhook Auto-Submission Triggers**:
   - Inspect CMS integration (WordPress IndexNow plugin, Cloudflare Crawler Hints, a custom Cloudflare Worker, Next.js publish hook, Shopify app, or custom webhook).
   - Cloudflare Crawler Hints and a custom Cloudflare IndexNow Worker are different setups. With Crawler Hints, Cloudflare notifies IndexNow at the edge and the origin hosts no key file at all, so origin key hosting is `NOT APPLICABLE`. A custom Worker that POSTs on the origin's behalf does require a `{key}.txt` file reachable on the origin.
   - Verify that URL updates, deletions, and 301 redirects automatically trigger a push.
   - Ensure non-200, draft, staging, and preview URLs are excluded from push batches.

4. **Classify Findings by Response Code & Deliver Remediation**:
   - Map each observed endpoint response to its spec meaning: `200` submitted, `202` accepted with key validation pending, `400` invalid format, `403` key invalid or key file not found, `422` URLs do not belong to the host or violate `keyLocation` path scoping, `429` rate-limited `[INDEXNOW-SPEC-01]`. Full table in `references/checks.md` §5.
   - Distinguishing `403` from `422` is the core diagnostic of this audit: `403` means the key file is missing or its body does not match the key, `422` means the key file is fine but scoped to the wrong path (or the URLs are off-host).
   - For a missing key: provide a conforming key and root placement instructions.
   - For failing pushes: provide the corrected payload, CMS plugin configuration, and reproducible verification commands from `references/checks.md`.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Passive sitemap coverage and discovery → `sitemap-discovery-audit`
- Technical crawler rules in robots.txt → `robots-ai-crawler-audit`
- Developer implementation tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Reports must contain:
1. **IndexNow Key Verification Status**: host, key-hosting mechanism, key file HTTP status, content match, key charset/length conformance.
2. **Submission Endpoint & Payload Configuration**: endpoint, payload fields, `keyLocation` path scoping vs. `urlList` paths, and the observed or expected response code.
3. **CMS & Webhook Push Integration**: what triggers a push, on which events, and what is excluded.
4. **Recommended Fixes & Implementation**: concrete key placement, payload corrections, and CMS/worker configuration.
5. **Verification Commands**: reproducible read-only curl commands.

Grade each dimension as `COMPLIANT`, `PARTIAL`, `MISSING`, `MALFORMED`, or `NOT APPLICABLE`.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for cross-cutting rules on outcome guarantees and factual evidence.

- Never submit URLs to a live IndexNow endpoint without explicit operator authorization. A POST to `api.indexnow.org` is a state-changing third-party action, not an inspection: it enters URLs into Bing's and Yandex's indexing queues. Audit the *configured* payload statically by default; perform a live submission only after the operator confirms they control the host, and only with a URL already published on that host (see `references/checks.md` §4).
- Report the observed HTTP status code for every network claim. Do not describe a submission as "rejected" or a host as "unverified" without naming the code that was returned.
- Do not report findings for mechanisms the protocol does not define; absence of a non-existent file is not a defect.

---
name: indexnow-instant-indexing-audit
description: Audit whether a website implements the IndexNow protocol for instant URL discovery and indexation by Bing, Yandex, Seznam, Naver, and AI search engines.
---

# IndexNow Instant Indexing & Discovery Audit

Audit whether a website provides real-time, push-based indexation and discovery capabilities to search engines and AI answer engines via the IndexNow protocol `[INDEXNOW-SPEC-01]`, moving beyond passive pull-based sitemap polling.

## Workflow

1. **Verify IndexNow Verification Key File Hosting**:
   - Check if an IndexNow key file is hosted at the domain root: `https://example.com/{key}.txt` `[INDEXNOW-SPEC-01]`.
   - Verify that the text content of `/{key}.txt` exactly matches the key string.
   - Inspect optional location declaration in `/indexnow.json` or HTTP header `X-IndexNow-Key`.
   - Verify that the key is at least 8 hexadecimal/alphanumeric characters.

2. **Audit Push Submission Payload & Key Matching**:
   - Check formatted POST payload to `https://api.indexnow.org/indexnow` (or `https://www.bing.com/indexnow` / `https://yandex.com/indexnow`) `[INDEXNOW-SPEC-01]`:
     - `host`: Target domain hostname (must match the key hosting domain).
     - `key`: The authentication key.
     - `keyLocation`: Optional explicit URL to the key file if not at domain root.
     - `urlList`: Array of newly published, modified, or deleted URLs (up to 10,000 URLs per call).

3. **Audit CMS & Webhook Auto-Submission Triggers**:
   - Inspect CMS integration (WordPress IndexNow plugin, Cloudflare Crawler Hints / IndexNow Worker, Next.js publish hook, Shopify app, or custom webhook).
   - Verify that URL updates, deletions, and 301 redirects automatically trigger an IndexNow push.
   - Ensure non-200 / draft / staging URLs are excluded from push batches.

4. **Classify Findings & Deliver Remediation**:
   - For missing key: generate an IndexNow key and provide placement instructions.
   - For failed endpoints: provide ready-to-run `curl` commands and CMS plugin configurations.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Passive sitemap coverage and discovery → `sitemap-discovery-audit`
- Technical crawler rules in robots.txt → `robots-ai-crawler-audit`
- Developer implementation tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Report status (`COMPLIANT`, `PARTIAL`, `MISSING`, or `MALFORMED`), key location, supported search engine endpoints, and implementation playbooks for Cloudflare, WordPress, and custom API backends.

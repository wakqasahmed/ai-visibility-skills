## Proposed llms.txt

```markdown
# DeveloperHub

> DeveloperHub gives teams instant APIs and developer tooling for building robust integrations.

## Overview

- [DeveloperHub Homepage](https://developer-hub.io/): Instant APIs and developer tooling platform.

## Documentation & API

- [Documentation](https://developer-hub.io/docs): Developer guides, concepts, and onboarding instructions.
- [API Reference](https://developer-hub.io/api): Complete API endpoints, parameters, and response schemas.

## Product & Pricing

- [Pricing](https://developer-hub.io/pricing): Usage tiers, plans, and developer quota limits.
```

## Placement path

`/llms.txt` at the site root (`https://developer-hub.io/llms.txt`). No existing file was found (404), so this is a clean initial placement.

## Source URLs used

- `https://developer-hub.io/`
- `https://developer-hub.io/docs`
- `https://developer-hub.io/api`
- `https://developer-hub.io/pricing`

All 4 URLs were spot-checked and verified to return HTTP 200.

## Missing recommended URLs or pages

- Support or FAQ page (`/support` or `/faq`)
- Privacy policy and terms of service pages (`/privacy`, `/terms`)

## [EXPERIMENTAL] Alternate discovery signals (Markdown content-negotiation, Auth.md / ARD manifest)

*Note: The following checks evaluate emerging draft standards surfaced by isitagentready.com. These signals are experimental and informational; absence of these records does not harm standard search or AI platform crawler indexing.*

- **Markdown Content Negotiation**: Enabled on `/docs` — server returns `content-type: text/markdown; charset=utf-8` when queried with `Accept: text/markdown`, allowing agents to fetch clean markdown without HTML stripping.
- **Auth.md / ARD Manifests**: `404` for `/auth.md` and `/.well-known/ard.json` — draft manifest files are not published, which is standard for current web deployments.

## Verification steps

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://developer-hub.io/llms.txt"
# expect: 200 after publishing
curl -sI "https://developer-hub.io/llms.txt" | grep -i content-type
# expect: text/plain or text/markdown, not text/html
curl -s "https://developer-hub.io/llms.txt" | grep -c '^## '
# expect: 3
curl -s -i -H "Accept: text/markdown" "https://developer-hub.io/docs" | grep -i "content-type"
```

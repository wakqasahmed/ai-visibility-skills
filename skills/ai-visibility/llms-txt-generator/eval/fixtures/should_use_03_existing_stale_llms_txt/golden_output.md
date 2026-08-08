An existing `llms.txt` already serves at `/llms.txt` (HTTP 200) with a homepage summary and a Docs section. I reviewed it before drafting a replacement rather than overwriting it blind. Its `/docs/api-v1` link now 404s — that page was replaced by `/docs/api-v2` per the current sitemap — so the update swaps the dead link for the verified replacement and adds the two new sitemap pages that weren't in the old file.

## Proposed llms.txt

```markdown
# HarborCloud

HarborCloud is managed Postgres hosting.

## Docs

- [Docs](https://harborcloud.io/docs): Product documentation.
- [API v2 Reference](https://harborcloud.io/docs/api-v2): Current API reference (replaces the retired v1 docs).

## Product

- [Pricing](https://harborcloud.io/pricing): Plans and pricing tiers.
- [Status](https://harborcloud.io/status): Live uptime and incident status.
```

## Placement path

`/llms.txt` at the site root — this replaces the existing file in place.

## Source URLs used

Homepage, `/docs`, `/docs/api-v2`, `/pricing`, and `/status` from `sitemap.xml`, each confirmed HTTP 200. `/docs/api-v1` was dropped: confirmed HTTP 404, superseded by `/docs/api-v2`.

## Missing recommended URLs or pages

None beyond the dead-link fix already applied.

## Verification steps

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://harborcloud.io/docs/api-v1"
# expect: 404 (confirms the old link is really dead, not a transient error)
curl -s -o /dev/null -w "%{http_code}\n" "https://harborcloud.io/docs/api-v2"
# expect: 200
curl -s "https://harborcloud.io/llms.txt" | grep -oE '\(https?://[^)]+\)'
# expect: no occurrence of /docs/api-v1
```

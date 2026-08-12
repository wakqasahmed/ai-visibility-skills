## Proposed llms.txt

```markdown
# QueueLayer

QueueLayer is a hosted message-queue API.

## Product

- [Docs](https://queuelayer.dev/docs): API reference and integration guides.
- [Status](https://queuelayer.dev/status): Live uptime and incident status.
```

## Placement path

`/llms.txt` at the site root. No existing file found (404) — new placement.

## Source URLs used

Homepage, `/docs`, and `/status` from `sitemap.xml`, each confirmed HTTP 200.

## Missing recommended URLs or pages

A pricing page is linked from the homepage nav but returns HTTP 404 and isn't in the sitemap — it appears to have never been published. Recommend publishing `/pricing` and adding it to this file once it returns 200; not included in the draft above since it doesn't resolve yet.

## Verification steps

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://queuelayer.dev/pricing"
# currently: 404 — re-run after publishing, then add to llms.txt if 200
curl -s "https://queuelayer.dev/llms.txt" | grep -oE '\(https?://[^)]+\)'
# expect: no /pricing until it resolves
```

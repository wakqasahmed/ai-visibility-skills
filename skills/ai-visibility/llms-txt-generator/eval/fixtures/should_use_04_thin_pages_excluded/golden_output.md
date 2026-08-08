## Proposed llms.txt

```markdown
# Fieldnote

Fieldnote is a personal blog covering gardening, travel, and food.

## Content

- [Archive](https://fieldnote.blog/archive): Full chronological post archive.
- [About](https://fieldnote.blog/about): Who writes Fieldnote and why.
```

## Placement path

`/llms.txt` at the site root. No existing file found (404) — new placement.

## Source URLs used

Homepage, `/archive`, and `/about` from `sitemap.xml`, each confirmed HTTP 200.

`/tag/gardening`, `/tag/travel`, and `/tag/food` were excluded: auto-generated tag-archive listings with no unique body copy beyond a repeated post-title list — thin, low-signal for an AI agent. `/archive?print=1` and `/archive?print=1&lang=en` were excluded as print-view duplicates of `/archive` with identical content.

## Missing recommended URLs or pages

None — the remaining pages already cover the site's actual content.

## Verification steps

```bash
curl -s "https://fieldnote.blog/llms.txt" | grep -oE '\(https?://[^)]+\)'
# expect: only /, /archive, /about — no /tag/* or ?print= URLs
```

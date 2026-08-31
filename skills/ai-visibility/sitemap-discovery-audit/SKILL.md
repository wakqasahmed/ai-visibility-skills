---
name: sitemap-discovery-audit
description: Audit sitemap coverage, canonical URLs, indexable pages, redirects, and crawl discovery paths. Use when a user wants AI search systems and crawlers to find the right pages.
---

# Sitemap Discovery Audit

Check whether crawlers can discover the site's important public URLs.

Scope: discovery paths only. Access rules (robots, headers, bot blocks) belong to `robots-ai-crawler-audit`; whole-site triage belongs to `ai-visibility-audit`.

## Workflow

1. Find the sitemap by following what the site itself declares, before guessing filenames:
   1. every `Sitemap:` directive in `robots.txt`, including ones pointing at another host;
   2. `<link rel="sitemap">` in the homepage `<head>` — how most SSG plugins advertise a
      non-default path;
   3. only then probe the common default paths (`/sitemap.xml`, `/sitemap_index.xml`,
      `/sitemap-index.xml`, and the rest of the list in `references/checks.md`).
   A filename guess-list on its own is not a discovery pass. Report "no sitemap found" only
   after all three steps come up empty, and name which step found it when one does.
2. Inspect sitemap indexes, URL sets, lastmod values, and obvious stale entries.
3. Compare sitemap URLs with navigation, important landing pages, docs, products, policies, and support pages.
4. Check representative URLs for status codes, redirects, canonical tags, and noindex. Compare the
   host in the sitemap's `<loc>` entries against the host that actually serves the site and the
   host its canonicals point at — a sitemap advertising a host that does not resolve, does not
   serve HTTPS, or is not the canonical host sends every crawler to a dead address.
5. Sweep internal links found on-page (not just sitemap entries) for broken/dead links — a link can 404 whether or not it is ever listed in the sitemap.
6. Identify missing, duplicate, blocked, broken, or low-value sitemap entries.

## Output

- Sitemap paths found
- Coverage gaps
- Broken or blocked URLs
- Canonical and redirect issues
- Priority fixes

"Broken or blocked URLs" covers both sitemap-listed entries and internal links discovered by crawling on-page navigation/body links — a broken-link sweep is not limited to what the sitemap happens to list.

## Check commands

See [`references/checks.md`](references/checks.md) for runnable commands, including
verifying `lastmod` delta direction against the reference audit date.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on not
claiming AI platform outcomes, not fabricating content, protecting private paths, and
chronological date/delta-direction arithmetic when comparing `lastmod` or other timestamps.

- Do not treat sitemap presence as proof of indexing.
- Do not conclude a sitemap is absent from a couple of default-path probes. Absence means
  `robots.txt`, the homepage `<head>` link, and the default-path list all came up empty — a
  sitemap living at a framework's own default (`gatsby-plugin-sitemap` writes
  `/sitemap-index.xml`, hyphenated) is a found sitemap, not a missing one.
- A `Sitemap:` directive missing from `robots.txt` is its own narrow finding. Report it as that,
  not as "no sitemap", when the sitemap was found another way.
- Flag a host mismatch between sitemap `<loc>` entries and the site's working/canonical host as a
  real discovery failure, not a cosmetic inconsistency.
- Prioritize high-value public pages over exhaustive URL counts.
- Flag generated or faceted URLs that may create crawl noise.

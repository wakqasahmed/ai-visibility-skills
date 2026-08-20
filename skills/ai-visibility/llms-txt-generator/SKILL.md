---
name: llms-txt-generator
description: Draft or review an `llms.txt` file from a site's public pages, docs, sitemap, products, policies, and support content. Use when a user wants AI agents to understand the most important URLs and context.
---

# llms.txt Generator

Create a concise `llms.txt` draft that points AI agents to the most useful public resources.

Scope: drafting and reviewing the file itself. Whether crawlers can reach it belongs to `robots-ai-crawler-audit`; choosing which pages deserve to exist belongs to `answer-engine-content-audit`.

## Workflow

1. Inspect the homepage, sitemap, docs, product/service pages, policy pages, and support pages.
2. Identify canonical high-value URLs and exclude thin, duplicate, private, or low-signal pages.
3. Group links by intent: overview, products/services, docs, support, policies, changelog, pricing, and contact.
4. Draft `llms.txt` with short descriptions for each section.
5. Note missing pages that would make the file more useful.
6. [EXPERIMENTAL] Check for emerging machine-readable discovery conventions (Markdown content-negotiation via `Accept: text/markdown` and Agential Resource Discovery manifests `/auth.md` or `/.well-known/ard.json`) — see `references/checks.md`. Clearly mark any findings as experimental draft standards.

## Output

- Proposed `llms.txt`
- Placement path: `/llms.txt`
- Source URLs used
- Missing recommended URLs or pages
- [EXPERIMENTAL] Alternate discovery signals (Markdown content-negotiation, Auth.md / ARD manifest) — clearly labeled as optional draft standards
- Verification steps

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on not
fabricating content and not exposing private/sensitive paths.

- Keep descriptions factual and brief.

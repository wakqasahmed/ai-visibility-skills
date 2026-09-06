---
name: answer-engine-content-audit
description: Find content gaps that prevent AI answer engines from explaining, comparing, recommending, or supporting a company, product, service, or site. Use for AEO, GEO, and AI search content planning.
---

# Answer Engine Content Audit

Assess whether a site answers the questions AI systems need to answer for users.

## Workflow

1. Identify target audience, offer, buying stage, and key decisions.
2. Review homepage, product/service pages, pricing, docs, comparison pages, FAQs, policies, and support content.
3. Map likely user questions to existing URLs.
4. Find missing, vague, outdated, or unciteable answers.
5. Check each reviewed page's `<title>` and meta description against length thresholds — these are the exact text AI answer engines and search snippets quote back to users, so a truncated or missing one is a citation-quality gap, not cosmetic.
   - **Cross-Check Hydrated DOM for Server-Rendered Content & Headings**: If raw HTML yields 0 `<h1>` or empty body containers on a JS-powered site, run a headless Chromium `--dump-dom` pass before declaring absence. If content exists only after JS execution, report as *Present in rendered DOM but absent from initial server response* (invisible to non-JS crawlers). If no browser is available, report as `[Derived]` with explicit disclosure.
6. Prioritize pages that improve recommendations, comparisons, objections, pricing clarity, and support automation.

## Output

- Question-to-URL map
- Missing high-intent answers
- Weak or vague answers
- Title/meta description length findings (see `references/checks.md`)
- Recommended page updates
- New page ideas with priority

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rule on not
fabricating unverifiable content.

- Prefer specific page edits over generic content advice.
- Keep recommendations tied to user questions and citation value.

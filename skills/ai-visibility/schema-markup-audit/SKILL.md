---
name: schema-markup-audit
description: Audit schema.org JSON-LD and structured data for AI search, answer engines, rich results, and agent understanding. Use for product, organization, article, FAQ, breadcrumb, offer, software, and local business pages.
---

# Schema Markup Audit

Review structured data for clarity, completeness, and consistency with visible page content.

## Workflow

1. Identify the page type and expected schema types.
2. Extract JSON-LD, microdata, or RDFa from representative pages. A raw-HTML pass that finds no
   JSON-LD does not mean the page is unmarked — re-extract from the hydrated DOM before
   concluding absence, and report the raw-vs-hydrated comparison (see `references/checks.md`).
3. Check required and useful properties for the page type.
4. Compare structured data against visible page content.
5. Check entity clarity: organization, product/service, author, offer, review, FAQ, breadcrumb, and contact details.
6. Prioritize fixes that improve disambiguation and answer confidence.

Use the extraction commands and per-type property checklists in `references/checks.md`.

## Output

- Existing schema types found — record how each block was delivered: raw HTML, hydrated DOM only, or both
- Missing or weak schema
- Mismatches with visible content
- Recommended JSON-LD changes
- Verification tools or commands

## Guardrails

- Do not report "no structured data" from a raw-HTML pass alone. Frameworks stream schema into the page after load (React Helmet, Next.js RSC payloads, `dangerouslySetInnerHTML`); a hydrated-DOM re-check must agree before absence is reported.
- Schema found only in the hydrated DOM is present, not missing — report it as present *and* as invisible to non-JS-executing crawlers. Both halves are the finding.
- Do not add schema claims that are not visible or supportable on the page.
- Separate rich-result eligibility from broader AI understanding.
- Prefer schema that clarifies real entities over decorative markup.

---
name: commerce-protocol-discovery
description: Check whether an ecommerce or marketplace site has any discoverable agentic-commerce/checkout-protocol surface — a UCP business profile, an A2A Agent Card, a protected MCP endpoint, or a machine-readable catalog feed. Use when a user wants to know if this is even a dimension worth checking, not a scored readiness or remediation audit.
---

# Commerce Protocol Discovery

Report what agentic-commerce discovery surface exists on an ecommerce or marketplace site —
nothing more. This is a **discovery-only teaser, not a readiness audit**: it never scores
protocols, never audits trust or checkout-lifecycle gates, and never recommends remediation
steps. Full commerce-protocol readiness scoring (a 5-state `ready`/`partial`/`missing`/`verified`
rubric, trust-and-order-lifecycle gates, and remediation recommendations) is a separate, deeper
audit capability that this skill does not attempt and must not reproduce.

Whole-site triage belongs to `ai-visibility-audit`; catalog-specific technical SEO (thin
category pages, faceted-nav duplicate URLs, orphan pages, discontinued-product handling)
belongs to `ecommerce-technical-seo-audit`; structured `Product`/`Offer` schema depth belongs
to `schema-markup-audit`. This skill only covers the four discovery probes below.

## Workflow

1. **Classify the site type.** If `ai-visibility-audit` already classified this site (SaaS,
   ecommerce, marketplace, docs, blog, local business, portfolio, enterprise), reuse that
   classification instead of re-deriving it. Otherwise classify it directly from observable
   signals: `Product`/`Offer` JSON-LD (schema.org) on representative pages, cart/checkout
   paths (`/cart`, `/checkout`), "add to cart" text in the raw HTML, or a platform-native
   catalog convention such as `/products.json`. Any one of these is sufficient to classify the
   site as ecommerce/marketplace.
2. If the site is **not** ecommerce/marketplace, stop here and say so — do not run the probes
   below on a site type they don't apply to.
3. If the site **is** ecommerce/marketplace, run exactly these four mechanical discovery
   probes from `references/checks.md`, in order:
   - UCP business profile at `/.well-known/ucp`
   - A2A Agent Card at `/.well-known/agent-card.json`
   - A protected MCP endpoint's `401` `WWW-Authenticate` challenge (only if an MCP endpoint is
     claimed or discoverable — never guess a site-root manifest)
   - Catalog feeds (`/products.json`, `/catalog.json`, and robots.txt/sitemap feed references)
4. Report each probe as: protocol/feed checked, endpoint probed, and the observed status
   code/result. Nothing else.

## Output

- Site-type classification and the signal(s) it was based on
- UCP business profile: endpoint probed, observed status code
- A2A Agent Card: endpoint probed, observed status code
- MCP: endpoint probed (if any was claimed/discoverable), observed challenge/status, or a note
  that none was claimed/discoverable to probe
- Catalog feeds: endpoint(s) probed, observed status code/result, and which convention (if any)
  matched
- Closing scope note (verbatim): "Full commerce-protocol readiness scoring and remediation is a
  separate audit capability — this section only reports what's discoverable, not whether it's
  implemented correctly or safely."

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on not claiming
AI platform outcome guarantees, not fabricating unverifiable claims, and not exposing
private/sensitive paths.

- Never use `ready`, `partial`, `missing`, or `verified` as a scoring label, and never use any
  other scoring language that implies a graded assessment — report only what was probed and
  what was observed.
- Never analyze trust gates, agent/user identity, payment authorization, or checkout/order
  lifecycle behavior — that is entirely out of scope for this skill.
- Never recommend a specific implementation or remediation step beyond the one closing scope
  sentence above — do not editorialize further.
- Do not probe a site-root MCP manifest path or guess one — only inspect a protected remote MCP
  endpoint's actual `401` challenge, and only when one is claimed or discoverable.

---
name: ai-visibility-audit
description: Audit whether ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews, and other AI agents can discover, understand, cite, and recommend a website using a 6-pillar decision-support scoring model.
---

# AI Visibility & Website Readiness Audit

Assess a public website for AI-mediated discovery, parsing, semantic understanding, answerability, and citation readiness using the standardized 6-pillar scoring architecture.

## Workflow

1. **Identify the site type**: SaaS, healthcare tech, ecommerce, marketplace, docs, blog, local business, portfolio, or enterprise.
2. **Pillar 1: Discovery (Weight: 20%)**: Audit `robots.txt`, XML sitemap availability/declaration, canonicals, redirect status, indexability, and crawler reachability.
3. **Pillar 2: Technical Accessibility (Weight: 20%)**: Audit server-delivered HTML payload, JavaScript dependency, semantic HTML structure, heading hierarchy, and performance/Core Web Vitals.
4. **Pillar 3: Machine Understanding (Weight: 20%)**: Audit Schema.org JSON-LD structured entities (`Organization`, `MedicalBusiness`, `Service`, `Product`), entity graph relationships, and `sameAs` authority links.
5. **Pillar 4: Answer Readiness (Weight: 20%)**: Test extractability of direct answers to high-intent customer questions from authoritative page content without model hallucination.
6. **Pillar 5: Trust & Authority (Weight: 15%)**: Audit verifiable company identity, leadership/author attribution, contact transparency, and case studies with quantified results.
7. **Pillar 6: Agent/Action Readiness (Weight: 5%)**: Audit conversion pathways, forms, documentation, machine-readable action endpoints, and optional agent guidance files.
8. **Classify Findings into 4 Evidence Tiers**:
   - *Tier 1 — Critical Foundation*: Directly blocks crawling, indexing, or core entity understanding.
   - *Tier 2 — Important Improvement*: Meaningfully impacts discoverability, answer extraction, or trust.
   - *Tier 3 — Supporting Signal*: General hygiene and secondary signals.
   - *Tier 4 — Experimental Protocol*: Emerging draft conventions (`llms.txt`, ARD, DNS-AID, Content Signals) — *never reduces the core 100-point audit score*.
9. **Separate Technical Hygiene**: Move transport security headers (HSTS, X-Content-Type-Options, clickjacking) into a dedicated non-scoring technical hygiene section.
10. **Produce Consolidated Deliverable**: Generate the executive 30-second dashboard, understand matrix, prioritized action plan (P0-P3), and technical appendix using `docs/templates/AUDIT_REPORT_TEMPLATE_V3.md`.

## Delegation

This is the orchestrator: it evaluates the 6 pillars, ranks blockers by evidence tier and priority, then hands deep dives to the focused specialist skills:

- Robots/meta-robots/header rules → `robots-ai-crawler-audit`
- Sitemap coverage, canonicals, redirects → `sitemap-discovery-audit`
- Structured data depth & Schema.org validation → `schema-markup-audit`
- Content answerability & heading hierarchy → `answer-engine-content-audit`
- Citation readiness, entity trust & authority → `citation-readiness-audit`
- Image alt text, image sitemap coverage & fetchability → `image-audit`
- Drafting `llms.txt` & agent markdown → `llms-txt-generator`
- For ecommerce sites: catalog spot-checks & faceted duplicate URLs → `ecommerce-technical-seo-audit`
- Generating remediation roadmap & developer tickets → `ai-search-remediation-plan`

## Output Format

Reports follow the V3 template in [`docs/templates/AUDIT_REPORT_TEMPLATE_V3.md`](../../docs/templates/AUDIT_REPORT_TEMPLATE_V3.md):
- **Executive Dashboard**: 30-second summary with overall score (0-100), 6-pillar scorecards, strengths, limitations, and top 3 priority actions.
- **What AI Can Understand Today**: `YES` / `PARTIAL` / `NO` diagnostic matrix and Business-Topic Extractability Map.
- **Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), P3 (Optional/Experimental) backlog.
- **6-Pillar Detailed Findings**: "Single Finding, Multiple Evidence" issue cards.
- **Technical Hygiene & Origin Security**: Isolated supporting header checks.
- **[EXPERIMENTAL] Emerging Agent Protocols**: Optional draft standards.
- **Technical Appendix**: Developer tickets with delegate skills, blueprints, and verification commands.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rule on not claiming AI platform outcome guarantees.

- Distinguish observed page evidence (`High [Measured]`) from inferred recommendations (`Medium [Derived]`).
- Emerging/experimental protocols (`llms.txt`, ARD) must never be presented as mandatory or reduce the core visibility score.
- Prefer public crawlable evidence unless the user provides private analytics or Search Console data.

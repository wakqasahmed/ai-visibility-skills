---
name: ai-visibility-audit
description: Audit whether ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews, and other AI agents can discover, understand, cite, and recommend a website using a 6-pillar decision-support scoring model.
---

# AI Visibility & Website Readiness Audit

Assess a public website for AI-mediated discovery, parsing, semantic understanding, answerability, and citation readiness using the standardized 6-pillar scoring architecture.

## Workflow

1. **Identify the site type & capability gating**:
   - Classify business model: SaaS, ecommerce, publisher/media, developer platform, healthcare, blog, local business, or enterprise.
   - **Capability Gating Matrix**:
     - *Ecommerce*: Catalog, product listings, cart, checkout, or facet filters detected → triggers `ecommerce-technical-seo-audit` & `commerce-protocol-discovery`. (If absent, catalog/facet checks are `N/A` with 0 pt deduction).
     - *Multilingual / Multi-Region*: Language subdirectories (`/es/`, `/de/`), localized subdomains, language selector menus, or `hreflang` tags detected → triggers `international-seo-hreflang-audit`. (If absent, hreflang checks are `N/A` with 0 pt deduction).
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
10. **Score Each Pillar Mechanically**: Apply [`references/scoring_rubric.md`](references/scoring_rubric.md) — never write a pillar score as a free-form estimate. Each pillar starts at 100 and loses only the specific, rationale-backed deductions the rubric's table lists for checks actually triggered by this audit's findings. Mark any check that doesn't apply to this site type as N/A rather than scoring it a pass or a fail; if every check in a pillar is N/A, exclude that pillar and reproportion the remaining weights per the rubric's "Handling inapplicable checks and pillars" section. Show the check-by-check derivation in the report so the score is traceable, not asserted.
11. **Produce Consolidated Deliverable**: Generate the executive 30-second dashboard, understand matrix, prioritized action plan (P0-P3), and technical appendix using [`references/audit_report_template_v3.md`](references/audit_report_template_v3.md).

## Delegation & Specialist Skills

This skill serves as the central orchestrator: it evaluates the 6 pillars, ranks blockers by evidence tier and priority, and synthesizes outputs from the focused specialist skills.

**Invocation mechanism**: The specialist skills listed below are instruction sets (skills), not standalone agent identities. Run them within the current agent session, or reference the skill by name in the task text when spawning a generic sub-agent. Do NOT pass a skill name where a registered agent identity is expected (e.g. a sub-agent spawn tool's `agentId` parameter, as in OpenClaw's `sessions_spawn`) — that parameter only accepts registered agent identities, not skill names.

| Focus Area | Specialist Skill | Diagnostic Role & Outputs |
|---|---|---|
| **Discovery & Reachability** | `robots-ai-crawler-audit` | Evaluates `robots.txt`, meta robots tags, and header rules (access rules only). |
| **Sitemap & Indexing** | `sitemap-discovery-audit` | Audits sitemap availability, XML structure, canonicals, and redirect chains. |
| **Structured Data & Schema** | `schema-markup-audit` | Validates Schema.org JSON-LD depth, entity graph linkages, and `sameAs` authority. |
| **Content & Answer Extraction** | `answer-engine-content-audit` | Tests direct Q&A extractability, heading structure, and content specificity. |
| **Citation & Brand Authority** | `citation-readiness-audit` | Checks entity disambiguation, author credentials, and verifiable client proof. |
| **Visual Asset Accessibility** | `image-audit` | Checks image alt text, server renderability, and image sitemap coverage. |
| **International & Multi-Region** | `international-seo-hreflang-audit` | Audits bidirectional hreflang tags, x-default fallbacks, language codes, and canonical relationships across locales. |
| **Agent Context Manifest** | `llms-txt-generator` | Generates and validates `/llms.txt`; [EXPERIMENTAL] markdown content-negotiation and ARD manifests. |
| **Ecommerce Catalog Health** | `ecommerce-technical-seo-audit` | Audits thin category pages, faceted-navigation duplicate URLs, orphan product URLs, and discontinued-product handling (ecommerce only). |
| **Commerce Agent Discovery** | `commerce-protocol-discovery` | Discovers UCP profiles, A2A cards, MCP endpoints, and feeds (ecommerce/marketplace only; discovery, not remediation). |
| **Remediation Roadmap** | `ai-search-remediation-plan` | Translates audit findings into prioritized developer tickets with blueprints. |

## Output Format

Reports follow the V3 template in [`references/audit_report_template_v3.md`](references/audit_report_template_v3.md), scored per [`references/scoring_rubric.md`](references/scoring_rubric.md):
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

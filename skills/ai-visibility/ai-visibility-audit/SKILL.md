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
     - *Developer / API Platform*: Developer portal (`/docs`, `/api`, `/developers`), SDK reference guides, or exposed API endpoints detected → triggers `docs-api-visibility-audit`. (If absent, API schema checks are `N/A` with 0 pt deduction).
     - *Paywalled / Subscription*: Metered paywall, subscription barrier, premium membership gating, or `isAccessibleForFree` detected → triggers `paywall-access-audit`. (If absent, paywall checks are `N/A` with 0 pt deduction).
     - *Ambiguous Entity / Topic-Clustered Content*: A brand name that collides with same-named entities in other industries, an `Organization` entity with no `sameAs` or no stable `@id`, or a pillar-and-cluster content structure (hub pages with supporting subtopic articles) → triggers `semantic-entity-topical-map-audit`. Division of labour with `schema-markup-audit`: that skill validates whether entity types and properties are present and well-formed; this one asks whether the declared identity is *reconcilable* (stable `@id`, resolvable `sameAs` reference pages, `@id` reuse across nested entities) and whether topical clusters are actually interlinked. (If the site declares no `Organization` entity at all, rubric 3.1 already covers that and this skill adds nothing — skip it.)
     - *Client-Rendered / Hydrated*: Framework hydration markers in the raw HTML (`data-react-helmet`, `self.__next_f.push(`, `__NEXT_DATA__`, `window.__NUXT__`, `ng-version`, or a `<div id="root">`/`<div id="__next">` shell with no server-rendered body copy) → some head/body content is only assembled after JavaScript runs, so raw-HTML pattern matching under-reports it. Turns on step 2's fallback for every title/meta/canonical/JSON-LD check. (If absent, step 2's zero-match rule still applies — these markers are a hint, not the gate.)
2. **Rendering-mode fallback verification (title, meta description, canonical, JSON-LD)**: A raw-HTML pass that finds **zero** matches for any of these four is not a finding yet — it is an unresolved check. Re-run it against the hydrated DOM (headless Chromium `--dump-dom`, per [`references/checks.md`](references/checks.md) § "Hydrated-DOM fallback verification") before concluding absence, and report "absent" only when both passes agree.
   - If the two passes **differ**, report both as one finding: present in the hydrated DOM but absent from the initial server response, therefore invisible to non-JS-executing crawlers (GPTBot, ClaudeBot, PerplexityBot). Never silently reconcile to the hydrated answer — the divergence is itself the finding, and it scores as a Pillar 2 delivery failure (rubric 2.8), not as a Pillar 3 absence.
   - Attribute order is not guaranteed: match `<meta ... name="description"` and `<script ... application/ld+json` with the attribute anywhere inside the tag, never as a fixed adjacent-token string — framework attributes such as `data-react-helmet="true"` routinely sit between the tag name and the attribute being matched.
   - Record which pass produced each value (`raw HTML`, `hydrated DOM`, or `both`) on the evidence line, so the result is reproducible and the crawler-visibility question stays answerable.
   - If **no Chromium-family browser is available in the runtime**, the fallback cannot run at all. The pack does not pin one — `scripts/render-audit-pdf.py` only auto-detects whichever of Chrome/Edge/Chromium is installed — so this case is real. A zero-match raw pass then stays unresolved: report it as `[Derived]` with an explicit "no browser available, hydration cross-check not performed" disclosure, never silently as "absent" and never as "present". Rubric 2.8 is `N/A` (the divergence cannot be observed), but the underlying rubric items are still scored from the raw pass and carry the `[Derived]` label, so items whose N/A column reads "Never" (3.1, 5.3) remain reachable.
3. **Pillar 1: Discovery (Weight: 20%)**: Audit `robots.txt`, XML sitemap availability/declaration, canonicals, redirect status, indexability, and crawler reachability.
4. **Pillar 2: Technical Accessibility (Weight: 20%)**: Audit server-delivered HTML payload, JavaScript dependency (including any raw-vs-hydrated divergence step 2 found), semantic HTML structure, heading hierarchy, and performance/Core Web Vitals.
5. **Pillar 3: Machine Understanding (Weight: 20%)**: Audit Schema.org JSON-LD structured entities (`Organization`, `MedicalBusiness`, `Service`, `Product`), entity graph relationships, and `sameAs` authority links. Structured data that step 2 found only in the hydrated DOM counts as present here — its invisibility to non-JS crawlers is scored under Pillar 2, not double-counted as a missing entity.
6. **Pillar 4: Answer Readiness (Weight: 20%)**: Test extractability of direct answers to high-intent customer questions from authoritative page content without model hallucination.
7. **Pillar 5: Trust & Authority (Weight: 15%)**: Audit verifiable company identity, leadership/author attribution, contact transparency, and case studies with quantified results.
8. **Pillar 6: Agent/Action Readiness (Weight: 5%)**: Audit conversion pathways, forms, documentation, machine-readable action endpoints, and optional agent guidance files.
9. **Classify Findings into 4 Evidence Tiers**:
   - *Tier 1 — Critical Foundation*: Directly blocks crawling, indexing, or core entity understanding.
   - *Tier 2 — Important Improvement*: Meaningfully impacts discoverability, answer extraction, or trust.
   - *Tier 3 — Supporting Signal*: General hygiene and secondary signals.
   - *Tier 4 — Experimental Protocol*: Emerging draft conventions (`llms.txt`, ARD, DNS-AID, Content Signals) — *never reduces the core 100-point audit score*.
10. **Separate Technical Hygiene**: Move transport security headers (HSTS, X-Content-Type-Options, clickjacking) into a dedicated non-scoring technical hygiene section.
11. **Score Each Pillar Mechanically**: Apply [`references/scoring_rubric.md`](references/scoring_rubric.md) — never write a pillar score as a free-form estimate. Each pillar starts at 100 and loses only the specific, rationale-backed deductions the rubric's table lists for checks actually triggered by this audit's findings. Mark any check that doesn't apply to this site type as N/A rather than scoring it a pass or a fail; if every check in a pillar is N/A, exclude that pillar and reproportion the remaining weights per the rubric's "Handling inapplicable checks and pillars" section. Show the check-by-check derivation in the report so the score is traceable, not asserted.
12. **Produce Consolidated Deliverable**: Generate the executive 30-second dashboard, understand matrix, prioritized action plan (P0-P3), and technical appendix using [`references/audit_report_template_v3.md`](references/audit_report_template_v3.md).

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
| **Developer Docs & API** | `docs-api-visibility-audit` | Audits OpenAPI spec discovery, server-rendered reference endpoints, and code sample markup. |
| **Paywall & Subscription** | `paywall-access-audit` | Audits Schema.org paywall markup, lead-in snippet SSR, and AI training vs. citation crawler policies. |
| **Entity Identity & Topical Map** | `semantic-entity-topical-map-audit` | Audits entity reconciliation (stable `@id`, resolvable `sameAs` reference pages, `@id` reuse across nested entities), author `Person` completeness, and pillar-cluster interlinking. Emits one `AMBIGUOUS`/`PARTIALLY_GROUNDED`/`FULLY_RECONCILED` classification, not a score. |
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
- Never report a title, meta description, canonical, or JSON-LD block as absent on the strength of a raw-HTML pass alone — an unverified zero-match is `[Derived]` at best, and only becomes `[Measured]` absence once the hydrated-DOM fallback in step 2 agrees.
- Emerging/experimental protocols (`llms.txt`, ARD) must never be presented as mandatory or reduce the core visibility score.
- Prefer public crawlable evidence unless the user provides private analytics or Search Console data.

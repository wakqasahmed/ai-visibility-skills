# feat(reporting): implement V3 6-pillar scoring, 4-tier evidence model, unified findings, and executive dashboard

**Labels:** `enhancement`, `reporting`, `scoring`, `template`

## Problem

The current V1/V2 audit reports (Issue #79) provide strong technical diagnostics, but their scoring and presentation models create several conceptual and usability problems for both business and technical audiences.

### 1. Flat or misleading scoring

Critical blockers, supporting signals, and emerging protocols can currently have disproportionate or equivalent influence on the final result.

For example:

* Missing crawl access or indexability can be as important as lower-impact signals.
* `llms.txt` may produce a `0` despite being an emerging/experimental convention rather than a proven requirement for AI retrieval or visibility.
* A strong image alt-text score can visually offset more important weaknesses such as missing structured business/service data.

This can cause clients to misdiagnose their actual AI visibility health.

### 2. Category mixing

General website security and technical hygiene findings are mixed into AI visibility scoring.

Examples:

* Missing HSTS
* Missing `X-Content-Type-Options`
* Missing clickjacking protections

These are legitimate findings, but they should not imply that they directly block LLM retrieval, AI understanding, or citation unless evidence specifically supports that relationship.

### 3. Audience conflict: skill-centric vs business-centric reporting

Reports currently expose internal implementation mechanics such as:

> Specialist Delegate: `schema-markup-audit`

before clearly explaining:

* What is wrong
* Why it matters to the business
* What impact it may have
* What should be done
* How urgent it is
* What outcome is expected

Business users should not need to understand the internal skill architecture to understand the report.

### 4. Duplicate findings across evidence sources

Different tools may report the same underlying problem independently.

For example:

* Crawler audit reports missing structured data.
* Schema validator reports no Organization schema.
* Lighthouse or another audit reports related SEO/structured-data concerns.

The report currently risks presenting these as separate findings rather than one consolidated issue supported by multiple pieces of evidence.

### 5. Lighthouse/PageSpeed Insights is not yet properly consolidated

Lighthouse provides valuable evidence about:

* Performance
* Accessibility
* Best Practices
* SEO
* Agentic Browsing

However, rendering Lighthouse as a parallel scorecard would duplicate information and overwhelm users.

Lighthouse should be treated as an **evidence provider**, with relevant findings mapped into the appropriate V3 pillars and consolidated with other audit evidence.

---

# Goal

Implement a V3 reporting architecture that transforms raw audit diagnostics into a clear, evidence-based decision system.

The final report MUST answer one central question:

> **What should this business do next to become easier for search engines, AI systems, and agents to find, understand, trust, answer questions about, and act upon?**

The report must be understandable by a business stakeholder within 30 seconds while preserving sufficient evidence and implementation detail for technical teams.

---

# Proposed V3 Architecture

## 1. Six-pillar scoring model

Replace the current flat scoring model with the following six pillars.

| Pillar                  | Weight | Primary Question                                                                    |
| ----------------------- | -----: | ----------------------------------------------------------------------------------- |
| Discovery               |    20% | Can systems find the website and its important pages?                               |
| Technical Accessibility |    20% | Can systems reliably access and read the content?                                   |
| Machine Understanding   |    20% | Can systems clearly understand the business, entities, services, and relationships? |
| Answer Readiness        |    20% | Can systems confidently answer relevant user questions using the site's content?    |
| Trust & Authority       |    15% | Is there sufficient evidence to trust, cite, or recommend the business?             |
| Agent/Action Readiness  |     5% | Can agents understand available actions and interact with the business effectively? |

### 1.1 Discovery — 20%

May include:

* Search crawler access
* Relevant AI crawler access
* `robots.txt`
* XML sitemap availability and validity
* Sitemap declaration
* Canonical URLs
* HTTP status and redirects
* Indexability signals
* Important-page discovery
* Internal linking

### 1.2 Technical Accessibility — 20%

May include:

* Server-delivered/raw HTML content
* JavaScript dependency
* Rendering requirements
* Semantic HTML
* Heading structure
* HTTP/page health
* Relevant performance findings
* Relevant accessibility findings

### 1.3 Machine Understanding — 20%

May include:

* Organization/entity identification
* Structured data presence and validity
* Organization schema
* WebSite schema
* Service/Product/SoftwareApplication schema where applicable
* Entity relationships
* `sameAs` relationships where applicable
* Consistency between visible content and structured data
* Machine-readable business identity

### 1.4 Answer Readiness — 20%

Measure whether important business questions can be answered clearly and directly from authoritative website content.

Examples:

* What does the company do?
* What services does it provide?
* Who is it for?
* Which industries does it serve?
* What products does it offer?
* Where does it operate?
* Why should a customer choose it?
* What evidence supports its expertise?

Evaluation SHOULD consider:

* Answer presence
* Clarity
* Directness
* Authoritativeness
* Supporting evidence
* Content freshness where measurable

### 1.5 Trust & Authority — 15%

May include:

* Clear company identity
* About/company information
* Team or expertise evidence
* Author information where relevant
* Contact information
* Case studies
* Testimonials
* Client evidence
* External mentions
* Relevant authority/backlink signals where available
* Content freshness
* Consistency of business identity

### 1.6 Agent/Action Readiness — 5%

May include:

* Clear contact/conversion paths
* Forms and action flows
* Product/service information
* Documentation
* Pricing/process information where relevant
* Structured action-relevant information
* Agent-readable policies where relevant

Emerging protocols such as `llms.txt` MUST be treated as optional/experimental signals unless there is strong evidence that they are required for the audited use case.

---

# 2. Four-tier evidence model

Every audit check and finding MUST be classified into one of four evidence tiers.

## Tier 1 — Critical Foundation

Signals that can directly prevent discovery, access, reading, or fundamental understanding.

Examples:

* Important content blocked from crawling
* Critical pages inaccessible
* Broken canonical/indexability configuration
* Important pages undiscoverable
* Required server-rendered content unavailable

Tier 1 findings MAY materially reduce the relevant pillar score.

## Tier 2 — Important Improvement

Signals with meaningful expected impact on discoverability, understanding, answerability, or trust.

Examples:

* Missing core Organization schema
* Missing relevant Service/Product schema
* Weak entity clarity
* Poor direct-answer coverage
* Missing XML sitemap

Tier 2 findings SHOULD materially influence relevant pillar scores.

## Tier 3 — Supporting Signal

Useful quality or supporting indicators that should not outweigh core fundamentals.

Examples may include:

* Image alt-text quality
* Supporting metadata
* Secondary semantic improvements
* Non-critical accessibility improvements

Tier 3 findings SHOULD have limited scoring influence.

## Tier 4 — Experimental / Emerging

New, optional, or insufficiently proven conventions.

Examples:

* `llms.txt`
* Emerging agent manifests
* Experimental AI discovery protocols
* Other conventions without established evidence of material impact

### Mandatory rule

> **Tier 4 findings MUST NOT materially reduce the core overall readiness score.**

Tier 4 findings MAY contribute to a separate:

* Experimental Readiness
* Emerging Protocols
* Future Optimization

section.

A site MUST NOT be classified as having poor AI visibility primarily because an experimental protocol is absent.

---

# 3. Unified "Single Finding, Multiple Evidence" model

The reporting pipeline MUST deduplicate related observations from all tools into a single canonical finding.

Instead of:

```text
Crawler finding: Organization schema missing
Schema validator finding: Organization schema missing
SEO finding: Machine-readable business data incomplete
```

Generate:

## Example unified finding

### Machine-readable business identity is incomplete

**Severity:** High
**Pillar:** Machine Understanding
**Evidence Tier:** Tier 2 — Important Improvement
**Priority:** P0
**Confidence:** High

**Business impact**

Search engines and AI systems must infer important business facts primarily from unstructured page content. This can reduce confidence when identifying what the company is, what it offers, and when it is relevant to a user's query.

**Technical explanation**

No validated Organization schema was detected, and relevant business/service relationships are not sufficiently exposed as structured data.

**Evidence**

* Crawler: business identity found primarily in visible page content
* Schema audit: no Organization schema detected
* Schema validation: no corresponding entity markup found
* Additional evidence: include only non-duplicative supporting observations

**Affected systems**

* Search engines
* AI retrieval systems
* AI assistants
* Agents requiring machine-readable business context

**Recommended action**

Add and validate appropriate Organization schema and relevant Service/Product/SoftwareApplication schema where applicable.

**Expected outcome**

Clearer machine-readable business identity and relationships.

**Verification**

Define measurable acceptance criteria.

---

## Required canonical finding fields

Every significant V3 finding SHOULD support:

```text
id
title
pillar
evidence_tier
severity
priority
confidence
status

business_impact
technical_explanation

evidence[]
affected_urls[]
affected_systems[]

recommendation
expected_outcome
implementation_owner

verification[]
sources[]
```

Internal skill/delegate information MAY be retained in machine-readable data or the technical appendix, but MUST NOT be required to understand the executive report.

---

# 4. Lighthouse/PageSpeed Insights consolidation

Lighthouse MUST be treated as an evidence source, not as a separate competing audit report.

## Mapping

| Lighthouse Area  | Primary V3 Destination                                           |
| ---------------- | ---------------------------------------------------------------- |
| Performance      | Technical Accessibility                                          |
| Accessibility    | Technical Accessibility or Tier 3 supporting findings            |
| SEO              | Discovery and/or Technical Accessibility                         |
| Best Practices   | Technical Hygiene / supporting findings unless directly relevant |
| Agentic Browsing | Agent/Action Readiness                                           |

### Consolidation rule

If Lighthouse and another audit source identify the same underlying issue, they MUST be merged into one canonical finding.

Example:

**Canonical finding:** Critical page experience is slow

**Evidence:**

* Lighthouse: LCP exceeds target
* Performance audit: largest resource delays rendering
* Crawler: affected page remains accessible and readable

**Interpretation:**

The page is machine-accessible, but slower delivery may negatively affect user experience and related search performance.

The report MUST NOT independently repeat the same issue in:

* Lighthouse section
* Performance section
* SEO section
* AI section

unless the additional presentation adds distinct information.

---

# 5. Separate core readiness from technical hygiene

Security and general technical hygiene findings MUST be separated from core AI/search visibility scoring unless there is direct evidence of an impact on discovery, access, understanding, or actionability.

Create a separate supporting section such as:

## Technical Hygiene & Security

Possible findings:

* HSTS
* `X-Content-Type-Options`
* Clickjacking protection
* Other security headers
* General browser best practices

Each finding MUST explain its actual impact.

Example:

> Missing HSTS should be addressed for security and transport protection. It is reported as technical hygiene and does not independently indicate that AI systems cannot retrieve or understand the website.

---

# 6. Executive dashboard

The V3 report MUST begin with a business-friendly executive dashboard.

## Required 30-second summary

The dashboard MUST clearly answer:

1. Can systems find us?
2. Can systems read us?
3. Can systems understand what we do?
4. Can systems answer important questions about us?
5. Can systems trust/cite us?
6. Can agents take action or interact with us effectively?

Example:

```text
AI & Website Readiness: 68/100 — Needs Improvement

Discovery                 82  Good
Technical Accessibility   88  Good
Machine Understanding     35  Needs Attention
Answer Readiness          64  Needs Improvement
Trust & Authority         58  Needs Improvement
Agent/Action Readiness    45  Developing
```

### Required dashboard sections

#### What is working

Maximum 3–5 concise strengths.

#### What is limiting visibility

Maximum 3–5 highest-impact issues.

#### Top recommended actions

Show the highest-priority actions first.

Example:

1. **P0:** Add structured business and service data.
2. **P0:** Publish and validate XML sitemap.
3. **P1:** Improve direct answers for high-value customer questions.

#### Score interpretation

The report MUST explain that the score represents audited website readiness signals, not a guarantee of rankings, AI mentions, citations, or traffic.

---

# 7. Business and technical audience separation

V3 MUST support two presentation layers.

## Layer A — Executive / Business Report

For each significant finding, show:

* What is wrong
* Why it matters
* Business impact
* Priority
* Recommended action
* Expected outcome
* Confidence

Avoid exposing:

* Internal skill names
* Agent delegation mechanics
* Raw commands
* Excessive protocol details

unless needed for understanding.

## Layer B — Technical Detail / Appendix

Include:

* Technical evidence
* Headers
* URLs
* Crawl evidence
* Schema output
* Lighthouse evidence
* Internal implementation guidance
* Validation commands
* Acceptance criteria
* Relevant specialist skill/delegate information

The technical layer MUST trace back to the corresponding canonical finding.

---

# 8. Prioritization model

Every actionable finding MUST receive a priority:

## P0 — Do Now

Critical blocker or high-confidence, high-impact improvement.

## P1 — Do Next

Important improvement with meaningful expected impact.

## P2 — Improve

Useful optimization that should follow core issues.

## P3 — Optional / Experimental

Low-impact, supporting, or emerging optimization.

Priority MUST consider:

```text
impact
evidence_tier
confidence
scope
implementation_effort
```

Priority MUST NOT be derived from a raw subscore alone.

---

# 9. Confidence and evidence transparency

Every significant finding MUST expose a confidence level:

* High
* Medium
* Low

The report SHOULD distinguish evidence types where possible:

* **Measured** — directly observed by the audit
* **Account Verified** — confirmed through connected first-party data
* **Derived** — conclusion based on multiple measured signals
* **Estimated** — heuristic or model-based assessment

Example:

> **Confidence: High — Measured**
>
> `/sitemap.xml` returned HTTP 404 during the audit.

vs.

> **Confidence: Medium — Derived**
>
> The absence of structured entity data and inconsistent service descriptions may reduce machine confidence in identifying the business's primary offerings.

The report MUST avoid presenting derived or estimated conclusions as absolute facts.

---

# 10. Report structure

The default V3 report SHOULD use this order:

## 1. Executive Dashboard

* Overall readiness
* Six pillar scores
* What is working
* What is limiting readiness
* Top 3 actions

## 2. What Systems Can Understand Today

A plain-language summary:

| Question                                      | Status             |
| --------------------------------------------- | ------------------ |
| Can they find the business?                   | Yes / Partial / No |
| Can they access and read the content?         | Yes / Partial / No |
| Can they understand what the business does?   | Yes / Partial / No |
| Can they answer important customer questions? | Yes / Partial / No |
| Can they trust or cite the business?          | Yes / Partial / No |
| Can agents identify available actions?        | Yes / Partial / No |

## 3. Prioritized Action Plan

| Priority | Action | Impact | Effort | Owner | Expected Outcome |
| -------- | ------ | ------ | ------ | ----- | ---------------- |

## 4. Six Pillar Analysis

Detailed consolidated findings grouped by pillar.

## 5. Technical Hygiene & Supporting Signals

Security and non-core supporting findings.

## 6. Experimental / Emerging Readiness

Optional protocols such as `llms.txt`.

These findings MUST NOT distort the core score.

## 7. Technical Appendix

Evidence, raw diagnostics, implementation guidance, validation, and internal technical metadata.

---

# Out of Scope

The following are intentionally NOT part of this reporting architecture issue and SHOULD be implemented as separate issues:

## Actual AI presence measurement

Examples:

* Whether a brand appears in ChatGPT answers
* Citation/mention tracking
* Positioning across AI systems
* Prompt/query testing

## Competitor benchmarking

Examples:

* Competitor schema comparison
* Answer coverage gaps
* Entity/trust comparison
* AI visibility gap analysis

## Connected first-party evidence

Examples:

* Google Search Console
* Bing Webmaster Tools
* Indexing status
* Search queries
* Impressions
* Clicks
* Crawl statistics

The V3 data model MAY be designed to accept these evidence sources later.

---

# Acceptance Criteria

## Scoring

* [ ] Exactly six core scoring pillars are implemented with documented weights.
* [ ] Pillar weights total 100%.
* [ ] Each check is classified into one of four evidence tiers.
* [ ] Tier 4 experimental signals cannot materially reduce the core overall readiness score.
* [ ] Tier 3 supporting signals cannot outweigh Tier 1 or Tier 2 issues.
* [ ] Security/hygiene signals do not automatically affect AI visibility scoring.

## Findings

* [ ] Related observations from multiple tools are deduplicated into canonical findings.
* [ ] A canonical finding supports multiple evidence sources.
* [ ] Every significant finding includes business impact and technical explanation.
* [ ] Every significant finding includes priority and confidence.
* [ ] Every actionable finding includes a recommendation and expected outcome.
* [ ] Findings can include verification/acceptance criteria.

## Lighthouse

* [ ] Lighthouse is consumed as an evidence provider rather than rendered as an independent duplicate report.
* [ ] Relevant Lighthouse findings map to V3 pillars.
* [ ] Duplicate Lighthouse and audit findings are consolidated.

## Executive experience

* [ ] The first report page can be understood by a non-technical stakeholder without knowledge of internal skills or agent architecture.
* [ ] The dashboard answers the six core readiness questions.
* [ ] The dashboard shows the top 3 highest-priority actions.
* [ ] Internal specialist delegate names are not shown in the executive summary.

## Report architecture

* [ ] Business and technical presentation layers are clearly separated.
* [ ] Technical evidence can be traced back to canonical findings.
* [ ] Experimental protocols appear in a separate section.
* [ ] The report clearly states that scores are readiness assessments, not guarantees of rankings, citations, mentions, or traffic.

---

# Expected Outcome

V3 should convert the current audit from a collection of technical diagnostics into a **clear, evidence-based business decision report**.

A business stakeholder should quickly understand:

> **What is working, what is limiting visibility, what matters most, and what should be done next.**

A technical stakeholder should still be able to trace every important conclusion back to:

> **Measured evidence → canonical finding → recommendation → verification criteria.**

The V3 reporting layer should remain compatible with future additions such as actual AI presence measurement, competitor benchmarking, and connected Google Search Console/Bing evidence without requiring another fundamental redesign.

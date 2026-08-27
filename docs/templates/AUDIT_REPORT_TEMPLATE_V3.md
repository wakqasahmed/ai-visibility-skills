<!-- Canonical copy. A bundled duplicate lives at skills/ai-visibility/ai-visibility-audit/references/audit_report_template_v3.md for self-contained single-skill installs (issue #91) — keep both in sync when editing either. -->

# AI Visibility & Website Readiness Audit: {{TARGET_URL}}

**Target Domain:** `{{TARGET_URL}}`  
**Audit Date:** {{AUDIT_DATE}}  
**Site Classification:** {{SITE_TYPE}}  
**Overall Readiness Score:** **{{OVERALL_SCORE}}/100** — `{{VERDICT}}` *(READY / NEEDS IMPROVEMENT / BLOCKED)*  

---

## 1. Executive Dashboard (The 30-Second Summary)

> **Readiness Statement:** {{EXECUTIVE_SUMMARY_TEXT}}  
> *Note: This score reflects audited discoverability, machine-readability, answerability, and trust signals. It represents readiness for search engines and AI systems, not a commercial guarantee of ranking, citations, or traffic.*
>
> **Every point on this page is traceable.** Each pillar score below is derived mechanically from the deduction table in [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) — not a free-form estimate. Section 4's "Score Derivation" subsection under each pillar lists the exact rubric check IDs and point deductions that produced that pillar's number. If a check does not apply to this site type (e.g. no ecommerce checks on a docs site), it is marked N/A there rather than silently scored as a pass or a fail — see the rubric's "Handling inapplicable checks and pillars" section for how N/A pillars are excluded and the remaining weights are reproportioned.

### Six-Pillar AI Visibility Scorecard

| {{DISCOVERY_SCORE}} | {{TECH_ACCESS_SCORE}} | {{UNDERSTANDING_SCORE}} | {{ANSWER_SCORE}} | {{TRUST_SCORE}} | {{AGENT_SCORE}} |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. Discovery (20%)** | **2. Tech Access (20%)** | **3. Understanding (20%)** | **4. Answer Ready (20%)** | **5. Trust (15%)** | **6. Agent Ready (5%)** |
| `{{DISCOVERY_BADGE}}` | `{{TECH_ACCESS_BADGE}}` | `{{UNDERSTANDING_BADGE}}` | `{{ANSWER_BADGE}}` | `{{TRUST_BADGE}}` | `{{AGENT_BADGE}}` |

### Executive Overview

#### 🟢 What Is Working Well
- **{{STRENGTH_1_TITLE}}**: {{STRENGTH_1_DESC}}
- **{{STRENGTH_2_TITLE}}**: {{STRENGTH_2_DESC}}
- **{{STRENGTH_3_TITLE}}**: {{STRENGTH_3_DESC}}

#### 🔴 What Is Limiting Visibility & Understanding
- **{{LIMITATION_1_TITLE}}**: {{LIMITATION_1_DESC}}
- **{{LIMITATION_2_TITLE}}**: {{LIMITATION_2_DESC}}
- **{{LIMITATION_3_TITLE}}**: {{LIMITATION_3_DESC}}

#### 🎯 Top 3 Priority Actions
1. **P0 (Immediate)**: **{{ACTION_1_TITLE}}** — {{ACTION_1_DESC}}
2. **P0 (Immediate)**: **{{ACTION_2_TITLE}}** — {{ACTION_2_DESC}}
3. **P1 (Next)**: **{{ACTION_3_TITLE}}** — {{ACTION_3_DESC}}

### Executive Briefing: Report Scope & Navigation
- **Pillar Deep-Dives**: Section 4 details root-cause diagnostics across Discovery, Technical Access, Structured Schema, Answer Extraction, Authority Proof, and Agent Action Readiness.
- **Actionable Remediation**: Section 3 and Section 7 provide prioritized engineering tickets (P0-P3) complete with code blueprints, curl validation commands, and acceptance criteria.
- **Evidence-Based Grounding**: Every check is classified by Evidence Tier (`CRITICAL FOUNDATION`, `IMPORTANT IMPROVEMENT`, `SUPPORTING SIGNAL`, `EXPERIMENTAL PROTOCOL`) with transparent confidence ratings.

---

<!-- PAGE BREAK: WHAT AI CAN UNDERSTAND TODAY -->

## 2. What AI & Search Systems Can Understand Today

| Core Discovery & Intelligence Question | Status | Current Reality & Machine Perception |
|---|:---:|---|
| **1. Can search and AI crawlers find the website?** | `{{UNDERSTAND_Q1_STATUS}}` | {{UNDERSTAND_Q1_NOTE}} |
| **2. Can AI systems access and parse raw page content?** | `{{UNDERSTAND_Q2_STATUS}}` | {{UNDERSTAND_Q2_NOTE}} |
| **3. Can machines understand the company and its services?** | `{{UNDERSTAND_Q3_STATUS}}` | {{UNDERSTAND_Q3_NOTE}} |
| **4. Can AI answer high-intent customer questions directly?** | `{{UNDERSTAND_Q4_STATUS}}` | {{UNDERSTAND_Q4_NOTE}} |
| **5. Can AI engines trust and cite the brand authoritatively?** | `{{UNDERSTAND_Q5_STATUS}}` | {{UNDERSTAND_Q5_NOTE}} |
| **6. Can autonomous agents discover conversion actions?** | `{{UNDERSTAND_Q6_STATUS}}` | {{UNDERSTAND_Q6_NOTE}} |

### Business-Topic Machine Extractability Map

| Business Knowledge Area | Discovered | Clear in HTML | Structured Schema | Freshness | Confidence |
|---|:---:|:---:|:---:|:---:|:---:|
| **Core Company Identity & What It Does** | `{{TOPIC_1_DISC}}` | `{{TOPIC_1_HTML}}` | `{{TOPIC_1_SCHEMA}}` | `{{TOPIC_1_FRESH}}` | `{{TOPIC_1_CONF}}` |
| **Target Industries & Use Cases** | `{{TOPIC_2_DISC}}` | `{{TOPIC_2_HTML}}` | `{{TOPIC_2_SCHEMA}}` | `{{TOPIC_2_FRESH}}` | `{{TOPIC_2_CONF}}` |
| **Specific Services & Solutions Catalog** | `{{TOPIC_3_DISC}}` | `{{TOPIC_3_HTML}}` | `{{TOPIC_3_SCHEMA}}` | `{{TOPIC_3_FRESH}}` | `{{TOPIC_3_CONF}}` |
| **Products / Proprietary Technology** | `{{TOPIC_4_DISC}}` | `{{TOPIC_4_HTML}}` | `{{TOPIC_4_SCHEMA}}` | `{{TOPIC_4_FRESH}}` | `{{TOPIC_4_CONF}}` |
| **Pricing, Engagement & Onboarding Process** | `{{TOPIC_5_DISC}}` | `{{TOPIC_5_HTML}}` | `{{TOPIC_5_SCHEMA}}` | `{{TOPIC_5_FRESH}}` | `{{TOPIC_5_CONF}}` |
| **Geographic Location & Operating Regions** | `{{TOPIC_6_DISC}}` | `{{TOPIC_6_HTML}}` | `{{TOPIC_6_SCHEMA}}` | `{{TOPIC_6_FRESH}}` | `{{TOPIC_6_CONF}}` |
| **Leadership, Team & Subject Matter Experts** | `{{TOPIC_7_DISC}}` | `{{TOPIC_7_HTML}}` | `{{TOPIC_7_SCHEMA}}` | `{{TOPIC_7_FRESH}}` | `{{TOPIC_7_CONF}}` |
| **Case Studies, Proven Results & Client Proof** | `{{TOPIC_8_DISC}}` | `{{TOPIC_8_HTML}}` | `{{TOPIC_8_SCHEMA}}` | `{{TOPIC_8_FRESH}}` | `{{TOPIC_8_CONF}}` |

---

<!-- PAGE BREAK: PRIORITIZED ACTION PLAN -->

## 3. Prioritized Action Plan

| Priority | Recommended Action | Pillar | Evidence Tier | Impact | Effort | Owner |
|---|---|---|---|---|---|---|
| **P0** | **{{PLAN_1_ACTION}}** | {{PLAN_1_PILLAR}} | `CRITICAL` | High | Low | {{PLAN_1_OWNER}} |
| **P0** | **{{PLAN_2_ACTION}}** | {{PLAN_2_PILLAR}} | `IMPORTANT` | High | Low | {{PLAN_2_OWNER}} |
| **P1** | **{{PLAN_3_ACTION}}** | {{PLAN_3_PILLAR}} | `IMPORTANT` | High | Medium | {{PLAN_3_OWNER}} |
| **P1** | **{{PLAN_4_ACTION}}** | {{PLAN_4_PILLAR}} | `IMPORTANT` | Medium | Medium | {{PLAN_4_OWNER}} |
| **P2** | **{{PLAN_5_ACTION}}** | {{PLAN_5_PILLAR}} | `SUPPORTING` | Medium | Low | {{PLAN_5_OWNER}} |
| **P3** | **{{PLAN_6_ACTION}}** | {{PLAN_6_PILLAR}} | `EXPERIMENTAL` | Low | Low | {{PLAN_6_OWNER}} |

---

<!-- PAGE BREAK: DETAILED 6-PILLAR AUDIT FINDINGS -->

## 4. Detailed Consolidated Audit Findings (6 Pillars)

### Pillar 1: Discovery — Can Systems Find the Website? (Weight: 20%)

> **Pillar Score:** `{{DISCOVERY_SCORE}}/100` — `{{DISCOVERY_BADGE}}`

**Score Derivation** *(rubric: [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) § Pillar 1)*

| Rubric Check | Result | Deduction |
|---|---|---|
| {{DISCOVERY_RUBRIC_CHECK_1}} | {{DISCOVERY_RUBRIC_RESULT_1}} | {{DISCOVERY_RUBRIC_DEDUCTION_1}} |
| {{DISCOVERY_RUBRIC_CHECK_2}} | {{DISCOVERY_RUBRIC_RESULT_2}} | {{DISCOVERY_RUBRIC_DEDUCTION_2}} |
| {{DISCOVERY_RUBRIC_CHECK_N}} | {{DISCOVERY_RUBRIC_RESULT_N}} | {{DISCOVERY_RUBRIC_DEDUCTION_N}} |
| **Baseline 100, total deductions** | | **{{DISCOVERY_TOTAL_DEDUCTION}} → {{DISCOVERY_SCORE}}/100** |

*List every applicable check from the rubric's Pillar 1 table, including passing checks with a `0` deduction — not only the ones that lost points. Mark N/A checks explicitly (`N/A — <reason>`) rather than omitting the row.*

#### Finding 1.1: {{FINDING_1_TITLE}}
- **Severity:** `{{FINDING_1_SEVERITY}}` *(CRITICAL / HIGH / MEDIUM / LOW)*
- **Evidence Tier:** `{{FINDING_1_TIER}}` *(Critical Foundation / Important Improvement / Supporting Signal)*
- **Priority:** `{{FINDING_1_PRIORITY}}` *(P0 / P1 / P2 / P3)*
- **Confidence:** `{{FINDING_1_CONFIDENCE}}` *(High [Measured] / Medium [Derived])*
- **Business Impact:** {{FINDING_1_BUSINESS_IMPACT}}
- **Technical Explanation:** {{FINDING_1_TECH_EXPLANATION}}
- **Evidence:**
  - `robots.txt`: {{FINDING_1_EVIDENCE_ROBOTS}}
  - `sitemap.xml`: {{FINDING_1_EVIDENCE_SITEMAP}}
  - `HTTP Status`: {{FINDING_1_EVIDENCE_HTTP}}
  - `Catalog Crawl Health (facets/orphans/discontinued, ecommerce sites only)`: {{FINDING_1_EVIDENCE_CATALOG}}
- **Affected Systems:** {{FINDING_1_AFFECTED_SYSTEMS}}
- **Recommended Action:** {{FINDING_1_RECOMMENDATION}}
- **Expected Outcome:** {{FINDING_1_EXPECTED_OUTCOME}}
- **Verification Criteria:**
  - [ ] {{FINDING_1_VERIFY_1}}
  - [ ] {{FINDING_1_VERIFY_2}}

---

### Pillar 2: Technical Accessibility — Can Systems Read It? (Weight: 20%)

> **Pillar Score:** `{{TECH_ACCESS_SCORE}}/100` — `{{TECH_ACCESS_BADGE}}`

**Score Derivation** *(rubric: [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) § Pillar 2)*

| Rubric Check | Result | Deduction |
|---|---|---|
| {{TECH_ACCESS_RUBRIC_CHECK_1}} | {{TECH_ACCESS_RUBRIC_RESULT_1}} | {{TECH_ACCESS_RUBRIC_DEDUCTION_1}} |
| {{TECH_ACCESS_RUBRIC_CHECK_N}} | {{TECH_ACCESS_RUBRIC_RESULT_N}} | {{TECH_ACCESS_RUBRIC_DEDUCTION_N}} |
| **Baseline 100, total deductions** | | **{{TECH_ACCESS_TOTAL_DEDUCTION}} → {{TECH_ACCESS_SCORE}}/100** |

#### Finding 2.1: {{FINDING_2_TITLE}}
- **Severity:** `{{FINDING_2_SEVERITY}}`
- **Evidence Tier:** `{{FINDING_2_TIER}}`
- **Priority:** `{{FINDING_2_PRIORITY}}`
- **Confidence:** `{{FINDING_2_CONFIDENCE}}`
- **Business Impact:** {{FINDING_2_BUSINESS_IMPACT}}
- **Technical Explanation:** {{FINDING_2_TECH_EXPLANATION}}
- **Evidence:**
  - `Raw HTML Payload`: {{FINDING_2_EVIDENCE_HTML}}
  - `Heading Hierarchy`: {{FINDING_2_EVIDENCE_HEADINGS}}
  - `Performance / Core Web Vitals`: {{FINDING_2_EVIDENCE_PERF}}
- **Affected Systems:** {{FINDING_2_AFFECTED_SYSTEMS}}
- **Recommended Action:** {{FINDING_2_RECOMMENDATION}}
- **Expected Outcome:** {{FINDING_2_EXPECTED_OUTCOME}}
- **Verification Criteria:**
  - [ ] {{FINDING_2_VERIFY_1}}

---

### Pillar 3: Machine Understanding — Can Systems Understand What You Do? (Weight: 20%)

> **Pillar Score:** `{{UNDERSTANDING_SCORE}}/100` — `{{UNDERSTANDING_BADGE}}`

**Score Derivation** *(rubric: [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) § Pillar 3)*

| Rubric Check | Result | Deduction |
|---|---|---|
| {{UNDERSTANDING_RUBRIC_CHECK_1}} | {{UNDERSTANDING_RUBRIC_RESULT_1}} | {{UNDERSTANDING_RUBRIC_DEDUCTION_1}} |
| {{UNDERSTANDING_RUBRIC_CHECK_N}} | {{UNDERSTANDING_RUBRIC_RESULT_N}} | {{UNDERSTANDING_RUBRIC_DEDUCTION_N}} |
| **Baseline 100, total deductions** | | **{{UNDERSTANDING_TOTAL_DEDUCTION}} → {{UNDERSTANDING_SCORE}}/100** |

#### Finding 3.1: {{FINDING_3_TITLE}}
- **Severity:** `{{FINDING_3_SEVERITY}}`
- **Evidence Tier:** `{{FINDING_3_TIER}}`
- **Priority:** `{{FINDING_3_PRIORITY}}`
- **Confidence:** `{{FINDING_3_CONFIDENCE}}`
- **Business Impact:** {{FINDING_3_BUSINESS_IMPACT}}
- **Technical Explanation:** {{FINDING_3_TECH_EXPLANATION}}
- **Evidence:**
  - `Schema Extraction`: {{FINDING_3_EVIDENCE_SCHEMA}}
  - `Entity Graphs`: {{FINDING_3_EVIDENCE_ENTITY}}
  - `sameAs Relationships`: {{FINDING_3_EVIDENCE_SAMEAS}}
- **Affected Systems:** {{FINDING_3_AFFECTED_SYSTEMS}}
- **Recommended Action:** {{FINDING_3_RECOMMENDATION}}
- **Expected Outcome:** {{FINDING_3_EXPECTED_OUTCOME}}
- **Verification Criteria:**
  - [ ] {{FINDING_3_VERIFY_1}}

---

### Pillar 4: Answer Readiness — Can Systems Answer Questions Using Your Content? (Weight: 20%)

> **Pillar Score:** `{{ANSWER_SCORE}}/100` — `{{ANSWER_BADGE}}`

**Score Derivation** *(rubric: [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) § Pillar 4)*

| Rubric Check | Result | Deduction |
|---|---|---|
| {{ANSWER_RUBRIC_CHECK_1}} | {{ANSWER_RUBRIC_RESULT_1}} | {{ANSWER_RUBRIC_DEDUCTION_1}} |
| {{ANSWER_RUBRIC_CHECK_N}} | {{ANSWER_RUBRIC_RESULT_N}} | {{ANSWER_RUBRIC_DEDUCTION_N}} |
| **Baseline 100, total deductions** | | **{{ANSWER_TOTAL_DEDUCTION}} → {{ANSWER_SCORE}}/100** |

#### Finding 4.1: {{FINDING_4_TITLE}}
- **Severity:** `{{FINDING_4_SEVERITY}}`
- **Evidence Tier:** `{{FINDING_4_TIER}}`
- **Priority:** `{{FINDING_4_PRIORITY}}`
- **Confidence:** `{{FINDING_4_CONFIDENCE}}`
- **Business Impact:** {{FINDING_4_BUSINESS_IMPACT}}
- **Technical Explanation:** {{FINDING_4_TECH_EXPLANATION}}
- **Evidence:**
  - `Direct Answer Sampling`: {{FINDING_4_EVIDENCE_ANSWERS}}
  - `FAQ / Q&A Sections`: {{FINDING_4_EVIDENCE_FAQ}}
  - `Content Specificity`: {{FINDING_4_EVIDENCE_SPECIFICITY}}
  - `Category/Collection Page Word Count (ecommerce sites only)`: {{FINDING_4_EVIDENCE_CATEGORY_THINNESS}}
- **Affected Systems:** {{FINDING_4_AFFECTED_SYSTEMS}}
- **Recommended Action:** {{FINDING_4_RECOMMENDATION}}
- **Expected Outcome:** {{FINDING_4_EXPECTED_OUTCOME}}
- **Verification Criteria:**
  - [ ] {{FINDING_4_VERIFY_1}}

---

### Pillar 5: Trust & Authority — Should Systems Trust & Cite You? (Weight: 15%)

> **Pillar Score:** `{{TRUST_SCORE}}/100` — `{{TRUST_BADGE}}`

**Score Derivation** *(rubric: [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) § Pillar 5)*

| Rubric Check | Result | Deduction |
|---|---|---|
| {{TRUST_RUBRIC_CHECK_1}} | {{TRUST_RUBRIC_RESULT_1}} | {{TRUST_RUBRIC_DEDUCTION_1}} |
| {{TRUST_RUBRIC_CHECK_N}} | {{TRUST_RUBRIC_RESULT_N}} | {{TRUST_RUBRIC_DEDUCTION_N}} |
| **Baseline 100, total deductions** | | **{{TRUST_TOTAL_DEDUCTION}} → {{TRUST_SCORE}}/100** |

#### Finding 5.1: {{FINDING_5_TITLE}}
- **Severity:** `{{FINDING_5_SEVERITY}}`
- **Evidence Tier:** `{{FINDING_5_TIER}}`
- **Priority:** `{{FINDING_5_PRIORITY}}`
- **Confidence:** `{{FINDING_5_CONFIDENCE}}`
- **Business Impact:** {{FINDING_5_BUSINESS_IMPACT}}
- **Technical Explanation:** {{FINDING_5_TECH_EXPLANATION}}
- **Evidence:**
  - `Entity Proof / About Page`: {{FINDING_5_EVIDENCE_ENTITY}}
  - `Case Studies & Proof Points`: {{FINDING_5_EVIDENCE_CASESTUDIES}}
  - `Author / Leadership Attribution`: {{FINDING_5_EVIDENCE_AUTHORS}}
- **Affected Systems:** {{FINDING_5_AFFECTED_SYSTEMS}}
- **Recommended Action:** {{FINDING_5_RECOMMENDATION}}
- **Expected Outcome:** {{FINDING_5_EXPECTED_OUTCOME}}
- **Verification Criteria:**
  - [ ] {{FINDING_5_VERIFY_1}}

---

### Pillar 6: Agent/Action Readiness — Can Agents Interact With You? (Weight: 5%)

> **Pillar Score:** `{{AGENT_SCORE}}/100` — `{{AGENT_BADGE}}`

**Score Derivation** *(rubric: [`docs/SCORING_RUBRIC.md`](../SCORING_RUBRIC.md) § Pillar 6)*

| Rubric Check | Result | Deduction |
|---|---|---|
| {{AGENT_RUBRIC_CHECK_1}} | {{AGENT_RUBRIC_RESULT_1}} | {{AGENT_RUBRIC_DEDUCTION_1}} |
| {{AGENT_RUBRIC_CHECK_N}} | {{AGENT_RUBRIC_RESULT_N}} | {{AGENT_RUBRIC_DEDUCTION_N}} |
| **Baseline 100, total deductions** | | **{{AGENT_TOTAL_DEDUCTION}} → {{AGENT_SCORE}}/100** |

*If this pillar is wholly N/A for the site type (e.g. no commerce or conversion actions exist to check), write `N/A — pillar excluded, remaining weights reproportioned per docs/SCORING_RUBRIC.md` here instead of a derivation table, and show the reproportioned weights used in the Overall Readiness Score calculation.*

#### Finding 6.1: {{FINDING_6_TITLE}}
- **Severity:** `{{FINDING_6_SEVERITY}}`
- **Evidence Tier:** `{{FINDING_6_TIER}}`
- **Priority:** `{{FINDING_6_PRIORITY}}`
- **Confidence:** `{{FINDING_6_CONFIDENCE}}`
- **Business Impact:** {{FINDING_6_BUSINESS_IMPACT}}
- **Technical Explanation:** {{FINDING_6_TECH_EXPLANATION}}
- **Evidence:**
  - `Contact / Booking Form Clarity`: {{FINDING_6_EVIDENCE_FORMS}}
  - `Machine-Readable Process Info`: {{FINDING_6_EVIDENCE_PROCESS}}
- **Affected Systems:** {{FINDING_6_AFFECTED_SYSTEMS}}
- **Recommended Action:** {{FINDING_6_RECOMMENDATION}}
- **Expected Outcome:** {{FINDING_6_EXPECTED_OUTCOME}}
- **Verification Criteria:**
  - [ ] {{FINDING_6_VERIFY_1}}

---

<!-- PAGE BREAK: TECHNICAL HYGIENE -->

## 5. Technical Hygiene & Origin Security (Non-Scoring Supporting Signals)

> **Context:** *These items represent general website security, transport encryption, and browser best practices. They are critical for technical hygiene and visitor safety, but are separated here because they are not primary blockers to AI engine discovery or natural language understanding.*

| Security / Hygiene Probe | Status | Observed Header / Configuration | Business & Security Explanation |
|---|:---:|---|---|
| **Strict-Transport-Security (HSTS)** | `{{SEC_HSTS_STATUS}}` | `{{SEC_HSTS_HEADER}}` | Enforces encrypted HTTPS connections. Recommended for technical hygiene. |
| **X-Content-Type-Options: nosniff** | `{{SEC_NOSNIFF_STATUS}}` | `{{SEC_NOSNIFF_HEADER}}` | Prevents MIME-type sniffing vulnerabilities. |
| **X-Frame-Options (Clickjacking defense)** | `{{SEC_FRAME_STATUS}}` | `{{SEC_FRAME_HEADER}}` | Protects users against iframe clickjacking attacks. |
| **Content Security Policy (CSP)** | `{{SEC_CSP_STATUS}}` | `{{SEC_CSP_HEADER}}` | Restricts unauthorized script execution. |

---

<!-- PAGE BREAK: EXPERIMENTAL AGENT PROTOCOLS -->

## 6. 🧪 [EXPERIMENTAL] Emerging Agent Protocols (Draft Standards)

> **Context:** *These checks evaluate emerging draft standards surfaced by `isitagentready.com` and agent discovery working groups. Absence of these signals does **not** harm search engine discovery, crawler indexing, or AI platform visibility today, and does **not** reduce the core 100-point audit score.*

| Emerging Protocol Probe | Status | Observed Finding & Details |
|---|:---:|---|
| **Curated Context File (`/llms.txt`)** | `{{LLMSTXT_STATUS}}` | {{LLMSTXT_NOTE}} |
| **Markdown Content Negotiation (`Accept: text/markdown`)** | `{{MD_STATUS}}` | {{MD_NOTE}} |
| **Content Signals in `robots.txt` (`Content-Signal:`)** | `{{CONTENT_SIGNAL_STATUS}}` | {{CONTENT_SIGNAL_NOTE}} |
| **Web Bot Auth Cryptographic Verification (`/.well-known/http-message-signatures-directory`)** | `{{BOT_AUTH_STATUS}}` | {{BOT_AUTH_NOTE}} |
| **Agential Resource Discovery (`/auth.md`, `/.well-known/ard.json`)** | `{{ARD_STATUS}}` | {{ARD_NOTE}} |
| **DNS-AID SVCB/HTTPS Discovery (`{{DOMAIN}}` HTTPS/SVCB records)** | `{{DNS_AID_STATUS}}` | {{DNS_AID_NOTE}} |

---

<!-- PAGE BREAK: TECHNICAL APPENDIX -->

## 7. Technical Appendix & Developer Implementation Tickets

### Ticket 1: {{TICKET_1_TITLE}}
- **Priority:** `{{TICKET_1_PRIORITY}}`
- **Pillar:** {{TICKET_1_PILLAR}}
- **Specialist Delegate Skill:** `{{TICKET_1_DELEGATE}}`
- **Target Files / Systems:** {{TICKET_1_TARGETS}}
- **Implementation Scope:** {{TICKET_1_SCOPE}}
- **Code / Schema Blueprint:**
  ```json
  {{TICKET_1_CODE_SNIPPET}}
  ```
- **Validation Command:**
  ```bash
  {{TICKET_1_VERIFY_CMD}}
  # Expected: {{TICKET_1_EXPECTED}}
  ```
- **Acceptance Criteria:**
  - [ ] {{TICKET_1_AC_1}}
  - [ ] {{TICKET_1_AC_2}}

### Ticket 2: {{TICKET_2_TITLE}}
- **Priority:** `{{TICKET_2_PRIORITY}}`
- **Pillar:** {{TICKET_2_PILLAR}}
- **Specialist Delegate Skill:** `{{TICKET_2_DELEGATE}}`
- **Target Files / Systems:** {{TICKET_2_TARGETS}}
- **Implementation Scope:** {{TICKET_2_SCOPE}}
- **Validation Command:**
  ```bash
  {{TICKET_2_VERIFY_CMD}}
  # Expected: {{TICKET_2_EXPECTED}}
  ```
- **Acceptance Criteria:**
  - [ ] {{TICKET_2_AC_1}}

### Ticket 3: {{TICKET_3_TITLE}}
- **Priority:** `{{TICKET_3_PRIORITY}}`
- **Pillar:** {{TICKET_3_PILLAR}}
- **Specialist Delegate Skill:** `{{TICKET_3_DELEGATE}}`
- **Target Files / Systems:** {{TICKET_3_TARGETS}}
- **Implementation Scope:** {{TICKET_3_SCOPE}}
- **Validation Command:**
  ```bash
  {{TICKET_3_VERIFY_CMD}}
  # Expected: {{TICKET_3_EXPECTED}}
  ```
- **Acceptance Criteria:**
  - [ ] {{TICKET_3_AC_1}}

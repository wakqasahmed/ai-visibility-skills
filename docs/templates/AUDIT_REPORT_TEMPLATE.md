# AI Visibility Audit Report: {{TARGET_URL}}

**Target Domain:** `{{TARGET_URL}}`  
**Audit Date:** {{AUDIT_DATE}}  
**Site Classification:** {{SITE_TYPE}}  
**Overall Readiness Verdict:** **{{VERDICT}}** *(Ready / Partially Ready / Blocked)*  

---

## Executive Summary

{{EXECUTIVE_SUMMARY_TEXT}}

### AI Visibility Scorecard

| [{{CRAWLER_SCORE}}]({{TARGET_URL}}) | [{{SCHEMA_SCORE}}]({{TARGET_URL}}) | [{{SITEMAP_SCORE}}]({{TARGET_URL}}) | [{{CONTENT_SCORE}}]({{TARGET_URL}}) | [{{AGENTIC_SCORE}}]({{TARGET_URL}}) |
|:---:|:---:|:---:|:---:|:---:|
| **Crawler Access** | **Structured Data** | **Sitemap & Discovery** | **On-Page Context** | **Agentic Probes [EXPERIMENTAL]** |
| `{{CRAWLER_BADGE}}` | `{{SCHEMA_BADGE}}` | `{{SITEMAP_BADGE}}` | `{{CONTENT_BADGE}}` | `{{AGENTIC_BADGE}}` |

### Core Signals Breakdown

| Dimension | Status | Key Finding | Specialist Delegate |
|---|---|---|---|
| **Crawler Access & Robots** | `{{CRAWLER_STATUS}}` | {{CRAWLER_SUMMARY}} | `robots-ai-crawler-audit` |
| **Sitemap & Discovery** | `{{SITEMAP_STATUS}}` | {{SITEMAP_SUMMARY}} | `sitemap-discovery-audit` |
| **Structured Data (JSON-LD)** | `{{SCHEMA_STATUS}}` | {{SCHEMA_SUMMARY}} | `schema-markup-audit` |
| **On-Page Context & Headings** | `{{CONTENT_STATUS}}` | {{CONTENT_SUMMARY}} | `answer-engine-content-audit` |
| **Citation & Entity Trust** | `{{CITATION_STATUS}}` | {{CITATION_SUMMARY}} | `citation-readiness-audit` |
| **Origin Security Headers** | `{{SECURITY_STATUS}}` | {{SECURITY_SUMMARY}} | `robots-ai-crawler-audit` |
| **Image Discoverability** | `{{IMAGE_STATUS}}` | {{IMAGE_SUMMARY}} | `image-audit` |
| **Machine Context (`llms.txt`)** | `{{LLMSTXT_STATUS}}` | {{LLMSTXT_SUMMARY}} | `llms-txt-generator` |

---

## Top Blockers

| # | Blocker | Severity | Impact Summary | Specialist Delegate |
|---|---|---|---|---|
| **1** | {{BLOCKER_1_TITLE}} | `CRITICAL` | {{BLOCKER_1_IMPACT}} | `{{BLOCKER_1_DELEGATE}}` |
| **2** | {{BLOCKER_2_TITLE}} | `HIGH` | {{BLOCKER_2_IMPACT}} | `{{BLOCKER_2_DELEGATE}}` |
| **3** | {{BLOCKER_3_TITLE}} | `MEDIUM` | {{BLOCKER_3_IMPACT}} | `{{BLOCKER_3_DELEGATE}}` |
| **4** | {{BLOCKER_4_TITLE}} | `MEDIUM` | {{BLOCKER_4_IMPACT}} | `{{BLOCKER_4_DELEGATE}}` |
| **5** | {{BLOCKER_5_TITLE}} | `LOW` | {{BLOCKER_5_IMPACT}} | `{{BLOCKER_5_DELEGATE}}` |

---

## Detailed Evidence & Observations

### 1. Crawler & User-Agent Access
- **Observed Command:** `for ua in GPTBot ClaudeBot PerplexityBot Google-Extended CCBot Amazonbot; do ...; done`
- **Observed Output:**
  ```text
  {{CRAWLER_CURL_OUTPUT}}
  ```
- **Analysis:** {{CRAWLER_ANALYSIS}}

### 2. `robots.txt` & Sitemap Directives
- **Observed Command:** `curl -s {{TARGET_URL}}/robots.txt`
- **Observed Output:**
  ```text
  {{ROBOTS_TXT_CONTENT}}
  ```
- **Analysis:** {{ROBOTS_ANALYSIS}}

### 3. Machine-Readable Structured Data (Schema.org JSON-LD)
- **Observed Command:** `curl -s {{TARGET_URL}} | grep -oE '<script type="application/ld\+json">[^<]*'`
- **Observed Output:**
  ```text
  {{SCHEMA_OUTPUT}}
  ```
- **Analysis:** {{SCHEMA_ANALYSIS}}

### 4. On-Page Context, Meta Tags & Heading Hierarchy
- **Title Tag:** `{{TITLE_TAG}}` ({{TITLE_LEN}} chars)
- **Meta Description:** `{{META_DESCRIPTION}}` ({{META_LEN}} chars)
- **Canonical URL:** `{{CANONICAL_URL}}`
- **Heading Structure:**
  - `<h1>`: {{H1_LIST}}
  - `<h2>`: {{H2_LIST}}
- **Server Renderability:** {{RENDER_ANALYSIS}}

### 5. Origin Security Headers
- **Observed Command:** `curl -sI {{TARGET_URL}}`
- **Observed Output:**
  - `Strict-Transport-Security`: `{{HSTS_STATUS}}`
  - `X-Content-Type-Options`: `{{NOSNIFF_STATUS}}`
  - `X-Frame-Options`: `{{FRAME_STATUS}}`
- **Analysis:** {{SECURITY_ANALYSIS}}

### 6. Image Alt Text & Discovery
- **Sample Scope:** {{IMAGE_SAMPLE_COUNT}} images sampled
- **Missing / Empty Alt Count:** {{IMAGE_MISSING_ALT_COUNT}}
- **Analysis:** {{IMAGE_ANALYSIS}}

---

## ⚡ Quick Wins

1. **{{WIN_1_TITLE}}**: {{WIN_1_DESC}}
2. **{{WIN_2_TITLE}}**: {{WIN_2_DESC}}
3. **{{WIN_3_TITLE}}**: {{WIN_3_DESC}}
4. **{{WIN_4_TITLE}}**: {{WIN_4_DESC}}
5. **{{WIN_5_TITLE}}**: {{WIN_5_DESC}}

---

## 🧪 [EXPERIMENTAL] Emerging Agent Signals (Draft Standards)

> *Note: These checks evaluate emerging draft standards surfaced by `isitagentready.com` and agent discovery working groups. Absence of these signals does **not** harm search engine discovery, crawler indexing, or AI platform visibility today.*

- **Markdown Content Negotiation (`Accept: text/markdown`):** `{{MD_NEGOTIATION_STATUS}}` — {{MD_NEGOTIATION_NOTE}}
- **Content Signals in `robots.txt`:** `{{CONTENT_SIGNALS_STATUS}}` — {{CONTENT_SIGNALS_NOTE}}
- **Web Bot Auth (`/.well-known/bot-auth`):** `{{BOT_AUTH_STATUS}}` — {{BOT_AUTH_NOTE}}
- **Agential Resource Discovery (`/auth.md`, `/.well-known/ard.json`):** `{{ARD_STATUS}}` — {{ARD_NOTE}}
- **DNS-AID (`_aid.{{DOMAIN}}`):** `{{DNS_AID_STATUS}}` — {{DNS_AID_NOTE}}

---

## 📋 Prioritized Remediation Roadmap

### Ticket 1: {{TICKET_1_TITLE}}
- **Priority:** {{TICKET_1_PRIORITY}}
- **Delegate Skill:** `{{TICKET_1_DELEGATE}}`
- **Scope & Action:** {{TICKET_1_SCOPE}}
- **Verification Command:**
  ```bash
  {{TICKET_1_VERIFY_COMMAND}}
  # expect: {{TICKET_1_EXPECT}} (was: {{TICKET_1_WAS}})
  ```

### Ticket 2: {{TICKET_2_TITLE}}
- **Priority:** {{TICKET_2_PRIORITY}}
- **Delegate Skill:** `{{TICKET_2_DELEGATE}}`
- **Scope & Action:** {{TICKET_2_SCOPE}}
- **Verification Command:**
  ```bash
  {{TICKET_2_VERIFY_COMMAND}}
  # expect: {{TICKET_2_EXPECT}} (was: {{TICKET_2_WAS}})
  ```

### Ticket 3: {{TICKET_3_TITLE}}
- **Priority:** {{TICKET_3_PRIORITY}}
- **Delegate Skill:** `{{TICKET_3_DELEGATE}}`
- **Scope & Action:** {{TICKET_3_SCOPE}}
- **Verification Command:**
  ```bash
  {{TICKET_3_VERIFY_COMMAND}}
  # expect: {{TICKET_3_EXPECT}} (was: {{TICKET_3_WAS}})
  ```

### Ticket 4: {{TICKET_4_TITLE}}
- **Priority:** {{TICKET_4_PRIORITY}}
- **Delegate Skill:** `{{TICKET_4_DELEGATE}}`
- **Scope & Action:** {{TICKET_4_SCOPE}}
- **Verification Command:**
  ```bash
  {{TICKET_4_VERIFY_COMMAND}}
  # expect: {{TICKET_4_EXPECT}} (was: {{TICKET_4_WAS}})
  ```

# AI Visibility Audit Report: {{TARGET_URL}}

**Target Domain:** `{{TARGET_URL}}`  
**Audit Date:** {{AUDIT_DATE}}  
**Site Classification:** {{SITE_TYPE}}  
**Overall Readiness Verdict:** `{{VERDICT}}` *(READY / PARTIALLY READY / BLOCKED)*  

---

## Executive Summary

{{EXECUTIVE_SUMMARY_TEXT}}

### Core AI Visibility Scorecard (8 Essential Dimensions)

| [{{CRAWLER_SCORE}}]({{TARGET_URL}}) | [{{SITEMAP_SCORE}}]({{TARGET_URL}}) | [{{SCHEMA_SCORE}}]({{TARGET_URL}}) | [{{CONTENT_SCORE}}]({{TARGET_URL}}) |
|:---:|:---:|:---:|:---:|
| **Crawler Access** | **Sitemap & Discovery** | **Structured Data** | **On-Page Context** |
| `{{CRAWLER_BADGE}}` | `{{SITEMAP_BADGE}}` | `{{SCHEMA_BADGE}}` | `{{CONTENT_BADGE}}` |
| [{{CITATION_SCORE}}]({{TARGET_URL}}) | [{{SECURITY_SCORE}}]({{TARGET_URL}}) | [{{IMAGE_SCORE}}]({{TARGET_URL}}) | [{{LLMSTXT_SCORE}}]({{TARGET_URL}}) |
| **Citation & Trust** | **Security Headers** | **Image Alt Text** | **llms.txt** |
| `{{CITATION_BADGE}}` | `{{SECURITY_BADGE}}` | `{{IMAGE_BADGE}}` | `{{LLMSTXT_BADGE}}` |

### Core Signals Breakdown

| Dimension | Status | Key Finding | Specialist Delegate |
|---|---|---|---|
| **Crawler Access & Robots** | `{{CRAWLER_BADGE}}` | {{CRAWLER_SUMMARY}} | `robots-ai-crawler-audit` |
| **Sitemap & Discovery** | `{{SITEMAP_BADGE}}` | {{SITEMAP_SUMMARY}} | `sitemap-discovery-audit` |
| **Structured Data (JSON-LD)** | `{{SCHEMA_BADGE}}` | {{SCHEMA_SUMMARY}} | `schema-markup-audit` |
| **On-Page Context & Headings** | `{{CONTENT_BADGE}}` | {{CONTENT_SUMMARY}} | `answer-engine-content-audit` |
| **Citation & Entity Trust** | `{{CITATION_BADGE}}` | {{CITATION_SUMMARY}} | `citation-readiness-audit` |
| **Origin Security Headers** | `{{SECURITY_BADGE}}` | {{SECURITY_SUMMARY}} | `robots-ai-crawler-audit` |
| **Image Discoverability** | `{{IMAGE_BADGE}}` | {{IMAGE_SUMMARY}} | `image-audit` |
| **Machine Context (`llms.txt`)** | `{{LLMSTXT_BADGE}}` | {{LLMSTXT_SUMMARY}} | `llms-txt-generator` |

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

### 1. Crawler & User-Agent Access {{CRAWLER_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **AI Bot Status (GPTBot, ClaudeBot, PerplexityBot)** | `{{CRAWLER_ITEM_1_STATUS}}` | {{CRAWLER_ITEM_1_NOTE}} |
| **WAF / Anti-Bot Captcha Interception** | `{{CRAWLER_ITEM_2_STATUS}}` | {{CRAWLER_ITEM_2_NOTE}} |
| **Search Engine Crawlers (Googlebot, Bingbot)** | `{{CRAWLER_ITEM_3_STATUS}}` | {{CRAWLER_ITEM_3_NOTE}} |

- **Observed Command:** `for ua in GPTBot ClaudeBot PerplexityBot CCBot Amazonbot; do ...; done`
- **Robots-only token:** Inspect `Google-Extended` in `robots.txt`; it has no separate HTTP user-agent to probe.
- **Observed Output:**
  ```text
  {{CRAWLER_CURL_OUTPUT}}
  ```
- **Analysis:** {{CRAWLER_ANALYSIS}}

---

### 2. `robots.txt` & Sitemap Directives {{ROBOTS_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **`robots.txt` Availability & Reachability** | `{{ROBOTS_ITEM_1_STATUS}}` | {{ROBOTS_ITEM_1_NOTE}} |
| **Public High-Value Paths Disallow Rules** | `{{ROBOTS_ITEM_2_STATUS}}` | {{ROBOTS_ITEM_2_NOTE}} |
| **Directive Syntax & Whitespace Hygiene** | `{{ROBOTS_ITEM_3_STATUS}}` | {{ROBOTS_ITEM_3_NOTE}} |
| **Sitemap Declaration in `robots.txt`** | `{{ROBOTS_ITEM_4_STATUS}}` | {{ROBOTS_ITEM_4_NOTE}} |
| **XML Sitemap Reachability (`/sitemap.xml`)** | `{{ROBOTS_ITEM_5_STATUS}}` | {{ROBOTS_ITEM_5_NOTE}} |

- **Observed Command:** `curl -s {{TARGET_URL}}/robots.txt`
- **Observed Output:**
  ```text
  {{ROBOTS_TXT_CONTENT}}
  ```
- **Analysis:** {{ROBOTS_ANALYSIS}}

---

### 3. Machine-Readable Structured Data (Schema.org JSON-LD) {{SCHEMA_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **JSON-LD Script Blocks Embedded** | `{{SCHEMA_ITEM_1_STATUS}}` | {{SCHEMA_ITEM_1_NOTE}} |
| **Organization Entity Linked** | `{{SCHEMA_ITEM_2_STATUS}}` | {{SCHEMA_ITEM_2_NOTE}} |
| **Services / Products Entity Depth** | `{{SCHEMA_ITEM_3_STATUS}}` | {{SCHEMA_ITEM_3_NOTE}} |
| **Domain-Specific Schema (Healthcare / Ecommerce / Local)** | `{{SCHEMA_ITEM_4_STATUS}}` | {{SCHEMA_ITEM_4_NOTE}} |

- **Observed Command:** `curl -s {{TARGET_URL}} | grep -oE '<script type="application/ld\+json">[^<]*'`
- **Observed Output:**
  ```text
  {{SCHEMA_OUTPUT}}
  ```
- **Analysis:** {{SCHEMA_ANALYSIS}}

---

### 4. On-Page Context, Meta Tags & Heading Hierarchy {{CONTENT_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **Title Tag Optimization & Length** | `{{CONTENT_ITEM_1_STATUS}}` | {{CONTENT_ITEM_1_NOTE}} |
| **Meta Description Presence** | `{{CONTENT_ITEM_2_STATUS}}` | {{CONTENT_ITEM_2_NOTE}} |
| **Heading Hierarchy (Single H1, Logical H2s)** | `{{CONTENT_ITEM_3_STATUS}}` | {{CONTENT_ITEM_3_NOTE}} |
| **Raw HTML Server-Renderability** | `{{CONTENT_ITEM_4_STATUS}}` | {{CONTENT_ITEM_4_NOTE}} |

- **Title Tag:** `{{TITLE_TAG}}` ({{TITLE_LEN}} chars)
- **Meta Description:** `{{META_DESCRIPTION}}` ({{META_LEN}} chars)
- **Canonical URL:** `{{CANONICAL_URL}}`
- **Heading Structure:**
  - `<h1>`: {{H1_LIST}}
  - `<h2>`: {{H2_LIST}}
- **Server Renderability:** {{RENDER_ANALYSIS}}

---

### 5. Origin Security Headers {{SECURITY_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **Strict-Transport-Security (HSTS)** | `{{SECURITY_ITEM_1_STATUS}}` | {{SECURITY_ITEM_1_NOTE}} |
| **X-Content-Type-Options: nosniff** | `{{SECURITY_ITEM_2_STATUS}}` | {{SECURITY_ITEM_2_NOTE}} |
| **X-Frame-Options (Clickjacking defense)** | `{{SECURITY_ITEM_3_STATUS}}` | {{SECURITY_ITEM_3_NOTE}} |

- **Observed Command:** `curl -sI {{TARGET_URL}}`
- **Analysis:** {{SECURITY_ANALYSIS}}

---

### 6. Image Alt Text & Discoverability {{IMAGE_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **Image `alt` Attribute Coverage** | `{{IMAGE_ITEM_1_STATUS}}` | {{IMAGE_ITEM_1_NOTE}} |
| **Non-Empty Descriptive Alt Ratio** | `{{IMAGE_ITEM_2_STATUS}}` | {{IMAGE_ITEM_2_NOTE}} |
| **Image Fetchability & CDN Access** | `{{IMAGE_ITEM_3_STATUS}}` | {{IMAGE_ITEM_3_NOTE}} |

- **Sample Scope:** {{IMAGE_SAMPLE_COUNT}} images sampled
- **Missing / Empty Alt Count:** {{IMAGE_MISSING_ALT_COUNT}}
- **Analysis:** {{IMAGE_ANALYSIS}}

---

### 7. Machine Resource Discovery (`llms.txt`) {{LLMSTXT_HEADER_BADGE}}

| Verification Probe | Status | Finding & Evidence |
|---|---|---|
| **`/llms.txt` Reachability** | `{{LLMSTXT_ITEM_1_STATUS}}` | {{LLMSTXT_ITEM_1_NOTE}} |
| **Content-Type (`text/plain` vs `text/html`)** | `{{LLMSTXT_ITEM_2_STATUS}}` | {{LLMSTXT_ITEM_2_NOTE}} |
| **High-Value URL Curation** | `{{LLMSTXT_ITEM_3_STATUS}}` | {{LLMSTXT_ITEM_3_NOTE}} |

- **Observed Command:** `curl -s -i {{TARGET_URL}}/llms.txt`
- **Analysis:** {{LLMSTXT_ANALYSIS}}

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

### Emerging Protocols Adoption Scorecard

| [{{AGENTIC_SCORE}}]({{TARGET_URL}}) |
|:---:|
| **Draft Protocols Implemented** |
| `{{AGENTIC_BADGE}}` |

| Emerging Protocol Probe | Status | Observed Finding & Details |
|---|---|---|
| **Markdown Content Negotiation (`Accept: text/markdown`)** | `{{MD_STATUS}}` | {{MD_NOTE}} |
| **Content Signals in `robots.txt` (`Content-Signal:`)** | `{{CONTENT_SIGNAL_STATUS}}` | {{CONTENT_SIGNAL_NOTE}} |
| **Web Bot Auth Cryptographic Verification (`/.well-known/http-message-signatures-directory`)** | `{{BOT_AUTH_STATUS}}` | {{BOT_AUTH_NOTE}} |
| **Agential Resource Discovery (`/auth.md`, `/.well-known/ard.json`)** | `{{ARD_STATUS}}` | {{ARD_NOTE}} |
| **DNS-AID SVCB/HTTPS Discovery (`{{DOMAIN}}` HTTPS/SVCB records)** | `{{DNS_AID_STATUS}}` | {{DNS_AID_NOTE}} |

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

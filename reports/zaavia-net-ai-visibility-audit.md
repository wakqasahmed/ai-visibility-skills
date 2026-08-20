# AI Visibility Audit Report: https://zaavia.net/

**Target Domain:** `https://zaavia.net/`  
**Audit Date:** August 20, 2026  
**Site Classification:** B2B Software Development & Healthcare Solutions (Static S3 + Amazon CloudFront CDN)  
**Overall Readiness Verdict:** `PARTIALLY READY`  

---

## Executive Summary

`zaavia.net` has **open, unrestricted crawler access** for all major AI search and answer-engine bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.), and its homepage copy is **server-rendered directly in HTML** rather than locked behind client-side JavaScript.

However, AI visibility is hindered by a **complete absence of structured data (JSON-LD)**, a **missing XML sitemap (`404`)**, a **missing `llms.txt` (`404`)**, and **missing origin security headers** on CloudFront.

### Core Signals Scorecard

| Dimension | Status | Key Finding | Specialist Delegate |
|---|---|---|---|
| **Crawler Access & Robots** | `PASS` | All 8 major AI crawlers return HTTP 200 with full content. | `robots-ai-crawler-audit` |
| **Sitemap & Discovery** | `FAIL` | `https://zaavia.net/sitemap.xml` returns 404; missing in robots.txt. | `sitemap-discovery-audit` |
| **Structured Data (JSON-LD)** | `FAIL` | 0 JSON-LD blocks found; missing Organization and Service schemas. | `schema-markup-audit` |
| **On-Page Context & Headings** | `PASS` | Clear H1 (`Software Development Company Karachi- Pakistan`) and 5 H2 sections. | `answer-engine-content-audit` |
| **Citation & Entity Trust** | `PARTIALLY READY` | Public claims present, but missing schema entity linkage. | `citation-readiness-audit` |
| **Origin Security Headers** | `FAIL` | Missing HSTS, X-Content-Type-Options, and X-Frame-Options. | `robots-ai-crawler-audit` |
| **Image Discoverability** | `PASS` | 38 images sampled; 100% carry valid alt text attributes. | `image-audit` |
| **Machine Context (`llms.txt`)** | `FAIL` | `https://zaavia.net/llms.txt` returns 404 Not Found. | `llms-txt-generator` |

---

## Top Blockers

| # | Blocker | Severity | Impact Summary | Specialist Delegate |
|---|---|---|---|---|
| **1** | **Zero Structured Data (JSON-LD)** | `CRITICAL` | AI search engines cannot extract unambiguous machine-readable entity identity, services, or healthcare products. | `schema-markup-audit` |
| **2** | **Missing XML Sitemap (`/sitemap.xml` 404)** | `HIGH` | Search and agent crawlers cannot discover deep URLs or verify freshness. | `sitemap-discovery-audit` |
| **3** | **Missing `llms.txt` (`/llms.txt` 404)** | `MEDIUM` | Autonomous agents lack a curated index of authoritative product and docs URLs. | `llms-txt-generator` |
| **4** | **Missing Origin Security Headers** | `MEDIUM` | CloudFront lacks HSTS and MIME-sniffing protection headers. | `robots-ai-crawler-audit` |
| **5** | **`robots.txt` Syntax Anomalies** | `LOW` | Trailing spaces in `Disallow: /users /` etc. risk path matching bugs. | `robots-ai-crawler-audit` |

---

## Detailed Evidence & Observations

### 1. Crawler & User-Agent Access
- **Observed Command:** `for ua in GPTBot ClaudeBot PerplexityBot Google-Extended CCBot Amazonbot; do ...; done`
- **Observed Output:**
  ```text
  GPTBot               Status: 200, Content-Length: 609380, Content-Type: text/html
  OAI-SearchBot        Status: 200, Content-Length: 609380, Content-Type: text/html
  ClaudeBot            Status: 200, Content-Length: 609380, Content-Type: text/html
  PerplexityBot        Status: 200, Content-Length: 609380, Content-Type: text/html
  Google-Extended      Status: 200, Content-Length: 609380, Content-Type: text/html
  CCBot                Status: 200, Content-Length: 609380, Content-Type: text/html
  Amazonbot            Status: 200, Content-Length: 609380, Content-Type: text/html
  Googlebot            Status: 200, Content-Length: 609380, Content-Type: text/html
  ```
- **Analysis:** All major AI crawlers have full public access to the homepage HTML without WAF rate-limiting or captchas.

### 2. `robots.txt` & Sitemap Directives
- **Observed Command:** `curl -s https://zaavia.net/robots.txt`
- **Observed Output:**
  ```text
  User-agent: *
  Disallow: /login/
  Disallow: /users /
  Disallow: /sessions /
  Disallow: /logout /
  Disallow: /signup /
  ```
- **Analysis:** Public marketing and content routes are open. However, trailing spaces exist on multiple `Disallow:` directives, and no `Sitemap:` reference is declared. Probing `https://zaavia.net/sitemap.xml` returns `HTTP 404` (`NoSuchKey` S3 error).

### 3. Machine-Readable Structured Data (Schema.org JSON-LD)
- **Observed Command:** `curl -s https://zaavia.net/ | grep -oE '<script type="application/ld\+json">[^<]*'`
- **Observed Output:**
  ```text
  [No JSON-LD blocks found]
  ```
- **Analysis:** Zero Schema.org entities exist on the homepage. Knowledge graphs have no structured data to link Zaavia to its brand name, services, healthcare software solutions, or physical location.

### 4. On-Page Context, Meta Tags & Heading Hierarchy
- **Title Tag:** `Software Development Company Karachi- Pakistan` (48 chars)
- **Meta Description:** `Software Development Company in Pakistan with Global presence, specializing in Healthcare Software Development & Productivity Tools - Get FREE Demo TODAY!` (164 chars)
- **Canonical URL:** `https://zaavia.net/` (Self-referencing canonical verified)
- **Heading Structure:**
  - `<h1>`: `Software Development Company Karachi- Pakistan`
  - `<h2>`: `Trusted by Healthcare Professionals`, `Why Businesses Choose Zaavia`, `What We Do`, `Our Products`, `What Our Clients are Saying?`
- **Server Renderability:** 609 KB of content is served directly in the initial HTML payload, ensuring full visibility for non-JavaScript crawlers.

### 5. Origin Security Headers
- **Observed Command:** `curl -sI https://zaavia.net/`
- **Observed Output:**
  ```text
  HTTP/1.1 200 OK
  Content-Type: text/html
  Server: AmazonS3
  X-Cache: Hit from cloudfront
  Strict-Transport-Security: [MISSING]
  X-Content-Type-Options: [MISSING]
  X-Frame-Options: [MISSING]
  ```
- **Analysis:** CloudFront serves S3 objects without an attached Response Headers Policy for HSTS, MIME sniffing protection (`nosniff`), or clickjacking defense.

### 6. Image Alt Text & Discovery
- **Sample Scope:** 38 images sampled across homepage
- **Missing / Empty Alt Count:** 0
- **Analysis:** Excellent compliance. All product logos, client badges, and hero imagery contain non-empty descriptive `alt` attributes.

---

## ⚡ Quick Wins

1. **Fix `robots.txt` trailing spaces:** Clean up `Disallow: /users/`, `/sessions/`, `/logout/`, `/signup/`.
2. **Publish `sitemap.xml`:** Deploy an XML sitemap to the S3 bucket and declare `Sitemap: https://zaavia.net/sitemap.xml` in `robots.txt`.
3. **Add `Organization` & `Service` JSON-LD:** Embed Schema.org JSON-LD on the homepage describing Zaavia, its healthcare software, and services.
4. **Draft & Deploy `/llms.txt`:** Place an `llms.txt` file at the root summarizing Zaavia's core services, products, and contact pages.
5. **Enable CloudFront Response Headers Policy:** Attach AWS managed `SecurityHeadersPolicy` to enforce HSTS and `X-Content-Type-Options: nosniff`.

---

## 🧪 [EXPERIMENTAL] Emerging Agent Signals (Draft Standards)

> *Note: These checks evaluate emerging draft standards surfaced by `isitagentready.com` and agent discovery working groups. Absence of these signals does **not** harm search engine discovery, crawler indexing, or AI platform visibility today.*

- **Markdown Content Negotiation (`Accept: text/markdown`):** `FAIL` — Server returns `Content-Type: text/html` (standard HTML).
- **Content Signals in `robots.txt`:** `MISSING` — No `Content-Signal:` header or directive declared.
- **Web Bot Auth (`/.well-known/bot-auth`):** `404` — Cryptographic bot authentication not deployed.
- **Agential Resource Discovery (`/auth.md`, `/.well-known/ard.json`):** `404` — Draft manifest files not published.
- **DNS-AID (`_aid.zaavia.net`):** `MISSING` — No TXT discovery record declared.

---

## 📋 Prioritized Remediation Roadmap

### Ticket 1: Implement Schema.org JSON-LD Structured Data
- **Priority:** `CRITICAL`
- **Delegate Skill:** `schema-markup-audit`
- **Scope & Action:** Add `Organization` and `ProfessionalService` JSON-LD to `index.html` with `name`, `url`, `logo`, `description`, `sameAs`, and `contactPoint`.
- **Verification Command:**
  ```bash
  curl -s https://zaavia.net/ | grep -q 'application/ld+json'
  # expect: 0 exit code (was: not found)
  ```

### Ticket 2: Generate and Publish XML Sitemap
- **Priority:** `HIGH`
- **Delegate Skill:** `sitemap-discovery-audit`
- **Scope & Action:** Upload valid `sitemap.xml` to S3 root and add `Sitemap: https://zaavia.net/sitemap.xml` to `robots.txt`.
- **Verification Command:**
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" https://zaavia.net/sitemap.xml
  # expect: 200 (was: 404)
  ```

### Ticket 3: Draft and Deploy `llms.txt`
- **Priority:** `MEDIUM`
- **Delegate Skill:** `llms-txt-generator`
- **Scope & Action:** Create `/llms.txt` linking to Zaavia's products, healthcare solutions, and contact channels.
- **Verification Command:**
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" https://zaavia.net/llms.txt
  # expect: 200 (was: 404)
  ```

### Ticket 4: Configure CloudFront Security Headers & Fix `robots.txt`
- **Priority:** `MEDIUM`
- **Delegate Skill:** `robots-ai-crawler-audit`
- **Scope & Action:** Remove whitespace typos in `robots.txt` Disallow lines, and enable CloudFront `SecurityHeadersPolicy` (`Strict-Transport-Security`, `X-Content-Type-Options: nosniff`).
- **Verification Command:**
  ```bash
  curl -sI https://zaavia.net/ | grep -iE "(strict-transport-security|x-content-type-options)"
  # expect: matching headers present (was: missing)
  ```

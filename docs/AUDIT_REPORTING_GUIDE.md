# Audit Reporting Guide (Markdown to PDF)

This guide documents the standardized audit report workflow for the `ai-visibility-skills` pack. Reports transform raw crawler diagnostics and validator outputs into a **6-Pillar Decision-Support Framework** with an executive dashboard and technical implementation appendix.

---

## 1. Reporting Architecture (V3)

Audit deliverables follow the V3 template defined in [`docs/templates/AUDIT_REPORT_TEMPLATE_V3.md`](templates/AUDIT_REPORT_TEMPLATE_V3.md).

### The Six Weighted Scoring Pillars

| Pillar | Weight | Primary Diagnostic Scope |
|---|:---:|---|
| **1. Discovery** | **20%** | Search and AI crawler access, `robots.txt`, XML sitemap availability/declaration, canonicals, redirect health, indexability. |
| **2. Technical Accessibility** | **20%** | Server-delivered raw HTML, JavaScript dependency, semantic HTML structure, heading hierarchy, performance & Core Web Vitals. |
| **3. Machine Understanding** | **20%** | Schema.org JSON-LD structured entities (`Organization`, `Service`, `Product`), entity validation, `sameAs` authority links. |
| **4. Answer Readiness** | **20%** | Direct extractability of answers to high-intent customer questions from authoritative page text without hallucination. |
| **5. Trust & Authority** | **15%** | Clear company identity, team/author attribution, contact transparency, case studies with quantified results, freshness. |
| **6. Agent/Action Readiness** | **5%** | Conversion paths, forms, documentation, machine-readable action endpoints, and optional agent guidance files. |

### Scores Are Rubric-Derived, Not Free-Form Estimates

Every pillar score is computed from the deterministic deduction table in
[`docs/SCORING_RUBRIC.md`](SCORING_RUBRIC.md), not estimated. The rubric maps each pillar to
the specific, real checks the specialist skills already run (e.g. "robots.txt blocks GPTBot
with `Disallow: /`" or "no `Product`/`Offer` schema on the primary offering"), assigns each
check a reasoned point deduction, and states explicitly how to handle a check — or an entire
pillar — that doesn't apply to a given site type (excluded and the remaining weights
reproportioned, never defaulted to full or zero marks). Two people applying the rubric to the
same finding set must land on the same score; if they don't, treat that as a rubric bug to
fix, not an acceptable range. The V3 template's Section 4 "Score Derivation" subsection under
each pillar is where that mechanical trace — check ID → observed result → points deducted —
is shown, so a reader can verify the number instead of taking it on faith.

Per [`docs/RUNNING_AN_AUDIT.md`](RUNNING_AN_AUDIT.md), this score is a readiness assessment
of audited signals, not a promise of AI platform rankings, citations, or traffic — that
caveat lives in the report's executive dashboard note and doesn't change because the score is
now traceable rather than free-form; traceability makes the score reproducible, not a
guarantee of outcomes.

---

## 2. Four-Tier Evidence Hierarchy

To prevent low-impact signals or emerging draft conventions from distorting the overall audit score, findings are classified into 4 evidence tiers:

1. **Tier 1 — Critical Foundation**: Blockers that directly prevent crawling, indexing, or core entity disambiguation (e.g. `robots.txt` disallows, missing sitemap, missing Schema.org `Organization`).
2. **Tier 2 — Important Improvement**: Meaningful improvements to semantic understanding, answer extraction, or trust (e.g. missing `Service` schema, indirect Q&A copy, thin case studies).
3. **Tier 3 — Supporting Signal**: General hygiene and quality indicators that do not independently decide AI ranking (e.g. image alt text ratios, non-critical accessibility tweaks).
4. **Tier 4 — Experimental Protocol**: Emerging conventions (`llms.txt`, Markdown content negotiation, Content Signals, ARD, DNS-AID) with no current ranking guarantee. **Mandatory Rule:** Tier 4 items *never* reduce the core 100-point audit score.

---

## 3. Two-Layer Presentation Structure

The V3 report is architected for both executive decision-makers and technical engineers:

### Layer A: Client Executive Dashboard
- **The 30-Second Summary**: Overall Readiness Score (0-100), 6-Pillar Scorecard Grid, "What Is Working", "What Is Limiting Visibility", and Top 3 Priority Actions.
- **What AI & Search Can Understand Today**: A clear `YES` / `PARTIAL` / `NO` diagnostic matrix answering core questions about machine perception.
- **Business-Topic Extractability Map**: Matrix of what factual knowledge AI can confidently extract about the company.
- **Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), and P3 (Optional) action backlog.

### Layer B: Technical Appendix & Developer Tickets
- **Consolidated Findings**: "Single Finding, Multiple Evidence" cards grouping multiple tool observations into unified root-cause issues.
- **Technical Hygiene & Origin Security**: Independent evaluation of security headers (HSTS, X-Content-Type-Options, clickjacking).
- **Implementation Tickets**: Engineer-ready tickets complete with specialist delegate skills, code/schema blueprints, curl validation commands, and acceptance criteria.

---

## 4. Templates Available

| Template | File | Description |
|---|---|---|
| **V3 (Current / Recommended)** | [`docs/templates/AUDIT_REPORT_TEMPLATE_V3.md`](templates/AUDIT_REPORT_TEMPLATE_V3.md) | 6-pillar scoring, 4 evidence tiers, executive dashboard, single-finding cards, and technical tickets. |
| **Scoring Rubric (required companion to V3)** | [`docs/SCORING_RUBRIC.md`](SCORING_RUBRIC.md) | The deduction table every V3 pillar score is computed from — check-by-check point values, rationale, and N/A/reweighting rules. Apply this alongside the V3 template; the template's `{{*_SCORE}}` placeholders should never be filled in without it. |
| **V2** | [`docs/templates/AUDIT_REPORT_TEMPLATE_V2.md`](templates/AUDIT_REPORT_TEMPLATE_V2.md) | 8-dimension scorecard with itemized check tables and section status indicators. |
| **V1** | [`docs/templates/AUDIT_REPORT_TEMPLATE.md`](templates/AUDIT_REPORT_TEMPLATE.md) | Flat 8-dimension checklist and quick wins. |

---

## 5. Rendering Markdown to PDF and HTML

The repository includes a zero-dependency CLI tool [`scripts/render-audit-pdf.py`](../scripts/render-audit-pdf.py) that renders any audit Markdown report into:
- A standalone styled **HTML document** (`.html`).
- An executive, print-perfect **PDF document** (`.pdf`) using local headless Chrome/Edge.

### Usage

```bash
# Render to matching HTML and PDF in the same directory:
python scripts/render-audit-pdf.py output/v3/my-audit.md

# Or specify an explicit output path:
python scripts/render-audit-pdf.py output/v3/my-audit.md dist/client-report.pdf
```

### Key Render Engine Features
- **Dynamic 6-Pillar Scorecards**: SVG circular score gauges with Lighthouse color thresholds.
- **Executive Callout Cards**: Custom styling for strengths (green), limitations (red), and priority actions (blue).
- **Badge Styling**: High-contrast pills for Priorities (`P0`, `P1`, `P2`, `P3`), Severities (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), Evidence Tiers, and Confidence ratings (`High [Measured]`, `Medium [Derived]`).
- **Print Pagination**: Automatic page breaks for executive summary, understand matrix, action plan, and technical appendix.

---

## 6. Saving and Storing Reports

Store generated client/site audit reports in the `output/` directory (which is automatically git-ignored to prevent site-specific audits and binary PDFs from polluting the repository):
- `output/v3/<domain>-ai-visibility-audit.md`
- `output/v3/<domain>-ai-visibility-audit.html`
- `output/v3/<domain>-ai-visibility-audit.pdf`

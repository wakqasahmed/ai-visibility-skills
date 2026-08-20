# Audit Reporting Guide (Markdown to PDF)

This guide documents the standardized audit report workflow for the `ai-visibility-skills` pack. Whenever an AI visibility, crawler, schema, or content audit is conducted, reports follow a consistent, client-ready structure and can be rendered to PDF.

---

## 1. Structure of an Audit Report

All audit deliverables adhere to the template defined in [`docs/templates/AUDIT_REPORT_TEMPLATE.md`](templates/AUDIT_REPORT_TEMPLATE.md):

1. **Document Header**: Target URL, Audit Date, Site Classification, and Overall Readiness Verdict (`READY`, `PARTIALLY READY`, `BLOCKED`).
2. **Executive Summary & Signals Scorecard**: High-level narrative summary plus a summary table showing status across all 8 core audit dimensions.
3. **Top 5 Blockers**: A prioritized severity table (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) mapping each blocker to its specialist delegate skill.
4. **Detailed Evidence & Observations**: Command-by-command crawl evidence with actual status codes, headers, and body snippets.
5. **Quick Wins**: Immediate actionable fixes that can be deployed rapidly.
6. **[EXPERIMENTAL] Emerging Agent Signals (Draft Standards)**: Gated status for early-stage discovery protocols (Content Signals, Web Bot Auth, DNS-AID, Markdown negotiation, Auth.md/ARD manifests).
7. **Prioritized Remediation Roadmap**: Verifiable engineering tickets with re-runnable verification commands and expected states.

---

## 2. Rendering Markdown to PDF and HTML

The repository includes a zero-dependency CLI tool [`scripts/render-audit-pdf.py`](../scripts/render-audit-pdf.py) that converts any audit Markdown report into:
- A standalone styled **HTML document** (`.html`).
- An executive, print-perfect **PDF document** (`.pdf`) using local headless Chrome/Edge.

### Usage

```bash
# Render to matching HTML and PDF in the same directory:
python scripts/render-audit-pdf.py output/my-audit.md

# Or specify a custom PDF output path:
python scripts/render-audit-pdf.py output/my-audit.md dist/client-report.pdf
```

### Supported Features
- **Modern Typography**: Embedded Inter and JetBrains Mono fonts.
- **Dynamic Status Badges**: Automatically renders `READY`, `PARTIALLY READY`, `BLOCKED`, `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `PASS`, `FAIL`, and `[EXPERIMENTAL]` as styled badges.
- **Clean Terminal Code Blocks**: Dark terminal theme with syntax headers.
- **Print Optimization**: A4 page margins, page-break avoidance on tables/tickets/cards, and running headers/footers with dynamic page numbering.

---

## 3. Saving and Storing Reports

Store generated client/site audit reports in the `output/` directory (which is automatically git-ignored to prevent site-specific audits and binary PDFs from polluting the repo history):
- `output/<domain>-ai-visibility-audit.md`
- `output/<domain>-ai-visibility-audit.html`
- `output/<domain>-ai-visibility-audit.pdf`


#!/usr/bin/env python3
"""render-audit-pdf.py

Transforms an AI Visibility audit Markdown document (v1 or v2 format) into a
beautifully styled, executive HTML document and renders it into a print-perfect
PDF using a local headless Chromium-based browser (Chrome, Edge, or Chromium).

Zero external pip dependencies required. Uses Python standard library + local browser.

Usage:
    python scripts/render-audit-pdf.py path/to/audit_report.md [path/to/output.pdf]
"""

import os
import sys
import re
import html
import math
import subprocess
import shutil
from pathlib import Path


def find_browser_executable() -> str | None:
    """Find a local Edge, Chrome, or Chromium browser executable."""
    candidates = []

    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        candidates.extend([
            os.path.join(prog_files_x86, "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(prog_files, "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(local_app, "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(prog_files, "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(prog_files_x86, "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(local_app, "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(prog_files, "BraveSoftware\\Brave-Browser\\Application\\brave.exe"),
        ])
    elif sys.platform == "darwin":
        candidates.extend([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ])
    else:  # Linux / Unix
        for bin_name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge", "brave-browser"]:
            found = shutil.which(bin_name)
            if found:
                candidates.append(found)

    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


def generate_gauge_card(raw_score: str, label_text: str, status_text: str) -> str:
    """Generates a Lighthouse-style circular score gauge card."""
    score_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', raw_score).strip().strip('`').strip('*')
    label_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', label_text).strip().strip('*')
    status_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', status_text).strip().strip('`')

    is_fraction = "/" in score_clean
    try:
        if is_fraction:
            num, den = score_clean.split("/")
            pct = (float(num) / float(den)) * 100
            score_display = score_clean
            color = "#8b5cf6"  # Purple for draft / experimental
            bg_color = "#f5f3ff"
        else:
            pct = float(score_clean)
            score_display = str(int(pct))
            if pct >= 90:
                color = "#0cce6b"  # Lighthouse green
                bg_color = "#f0fdf4"
            elif pct >= 50:
                color = "#ffa400"  # Lighthouse orange
                bg_color = "#fffbeb"
            else:
                color = "#ff4e42"  # Lighthouse red
                bg_color = "#fef2f2"
    except Exception:
        pct = 0
        score_display = score_clean
        color = "#64748b"
        bg_color = "#f8fafc"

    r = 23
    c = 2 * math.pi * r
    offset = c * (1.0 - (max(0.0, min(100.0, pct)) / 100.0))

    badge_class = "badge-low"
    if any(k in status_clean.upper() for k in ["PASS", "READY", "100", "✅"]):
        badge_class = "badge-pass"
    elif any(k in status_clean.upper() for k in ["FAIL", "BLOCKED", "0", "❌"]):
        badge_class = "badge-fail"
    elif any(k in status_clean.upper() for k in ["PARTIAL", "WARN", "⚠️"]):
        badge_class = "badge-partial"
    elif any(k in status_clean.upper() for k in ["EXP", "DRAFT", "OPTIONAL", "🧪"]):
        badge_class = "badge-exp"

    return f"""
    <div class="score-card" style="background: {bg_color}; border-color: {color}33;">
        <div class="gauge-container">
            <svg viewBox="0 0 58 58" class="gauge-svg">
                <circle cx="29" cy="29" r="{r}" class="gauge-bg" />
                <circle cx="29" cy="29" r="{r}" class="gauge-fill" style="stroke: {color}; stroke-dasharray: {c:.2f}; stroke-dashoffset: {offset:.2f};" />
            </svg>
            <div class="gauge-score" style="color: {color};">{html.escape(score_display)}</div>
        </div>
        <div class="gauge-label">{html.escape(label_clean)}</div>
        <div class="gauge-status"><span class="badge {badge_class}">{html.escape(status_clean)}</span></div>
    </div>
    """


def markdown_to_html(md_content: str, title: str = "AI Visibility Audit Report") -> str:
    """Parses markdown audit report into semantic HTML with rich CSS styling."""
    lines = md_content.splitlines()
    html_lines = []
    in_code_block = False
    code_lang = ""
    code_buffer = []
    in_table = False
    table_buffer = []
    in_list = False
    list_tag = "ul"

    def format_inline(text: str) -> str:
        text = html.escape(text)
        
        # Replace status badges (supporting emojis and v1/v2 tokens)
        text = re.sub(r'`(✅\s*PASS|PASS)`', r'<span class="badge badge-pass">✅ PASS</span>', text, flags=re.I)
        text = re.sub(r'`(⚠️\s*(?:WARN|PARTIAL)|PARTIALLY\s*READY|WARN|PARTIAL)`', r'<span class="badge badge-partial">⚠️ WARN</span>', text, flags=re.I)
        text = re.sub(r'`(❌\s*(?:FAIL|CRITICAL)|FAIL|CRITICAL|BLOCKED)`', r'<span class="badge badge-fail">❌ FAIL</span>', text, flags=re.I)
        text = re.sub(r'`(HIGH)`', r'<span class="badge badge-high">HIGH</span>', text, flags=re.I)
        text = re.sub(r'`(MEDIUM)`', r'<span class="badge badge-medium">MEDIUM</span>', text, flags=re.I)
        text = re.sub(r'`(LOW)`', r'<span class="badge badge-low">LOW</span>', text, flags=re.I)
        text = re.sub(r'`(READY)`', r'<span class="badge badge-ready">READY</span>', text, flags=re.I)
        text = re.sub(r'`(🧪\s*EXPERIMENTAL|EXPERIMENTAL|🧪\s*DRAFT|OPTIONAL\s*\(DRAFT\)|DRAFT\s*PROTOCOLS)`', r'<span class="badge badge-exp">🧪 EXPERIMENTAL</span>', text, flags=re.I)
        text = re.sub(r'\[EXPERIMENTAL\]', r'<span class="badge badge-exp">EXPERIMENTAL</span>', text)
        
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        return text

    def flush_table():
        nonlocal in_table, table_buffer
        if not in_table or not table_buffer:
            in_table = False
            table_buffer = []
            return ""
        
        rows = [r.strip() for r in table_buffer if r.strip()]
        if not rows:
            in_table = False
            table_buffer = []
            return ""

        # Check if this table is a Lighthouse Scorecard Table:
        # Detected when header row cells are numerical scores e.g. [100], 0, 50, 0/5
        header_raw_cols = [c.strip() for c in rows[0].strip('|').split('|')]
        is_scorecard = len(header_raw_cols) >= 1 and any(
            re.search(r'(\[\d+\]|\b\d{1,3}\b|\b\d/\d\b)', c) for c in header_raw_cols
        ) and len(rows) >= 3

        if is_scorecard:
            scores = header_raw_cols
            labels = [c.strip() for c in rows[2].strip('|').split('|')] if len(rows) > 2 else [""] * len(scores)
            statuses = [c.strip() for c in rows[3].strip('|').split('|')] if len(rows) > 3 else [""] * len(scores)

            out = ['<div class="score-gauge-grid avoid-break">']
            for s, l, st in zip(scores, labels, statuses):
                out.append(generate_gauge_card(s, l, st))
            out.append('</div>')
            in_table = False
            table_buffer = []
            return '\n'.join(out)

        out = ['<div class="table-container avoid-break"><table>']
        out.append('<thead><tr>')
        for col in header_raw_cols:
            out.append(f'<th>{format_inline(col)}</th>')
        out.append('</tr></thead><tbody>')

        # Data rows (skip separator row at index 1)
        for row_str in rows[2:]:
            cols = [c.strip() for c in row_str.strip('|').split('|')]
            out.append('<tr>')
            for col in cols:
                out.append(f'<td>{format_inline(col)}</td>')
            out.append('</tr>')

        out.append('</tbody></table></div>')
        in_table = False
        table_buffer = []
        return '\n'.join(out)

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Handle Code Fences
        if stripped.startswith("```"):
            if in_code_block:
                code_content = html.escape('\n'.join(code_buffer))
                html_lines.append(f'<div class="code-block"><div class="code-header"><span class="code-dot dot-red"></span><span class="code-dot dot-yellow"></span><span class="code-dot dot-green"></span><span class="code-lang">{code_lang or "bash"}</span></div><pre><code class="language-{code_lang}">{code_content}</code></pre></div>')
                code_buffer = []
                in_code_block = False
            else:
                if in_table:
                    html_lines.append(flush_table())
                if in_list:
                    html_lines.append(f"</{list_tag}>")
                    in_list = False
                in_code_block = True
                code_lang = stripped[3:].strip()
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Handle Markdown Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            in_table = True
            table_buffer.append(stripped)
            i += 1
            continue
        elif in_table:
            html_lines.append(flush_table())

        # Handle Horizontal Rules
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            html_lines.append('<hr class="divider"/>')
            i += 1
            continue

        # Handle Headings
        if stripped.startswith("#"):
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            
            level = len(re.match(r'^(#+)', stripped).group(1))
            heading_text = stripped[level:].strip()
            
            if level == 1:
                html_lines.append(f'<div class="doc-header"><div class="brand-pill">AI Visibility Audit</div><h1 class="doc-title">{format_inline(heading_text)}</h1></div>')
            elif level == 2:
                html_lines.append(f'<h2 class="section-title">{format_inline(heading_text)}</h2>')
            elif level == 3:
                # Check for status indicator in subsection title
                status_class = ""
                if "✅" in heading_text or "PASS" in heading_text:
                    status_class = "sub-pass"
                elif "⚠️" in heading_text or "WARN" in heading_text or "PARTIAL" in heading_text:
                    status_class = "sub-warn"
                elif "❌" in heading_text or "FAIL" in heading_text:
                    status_class = "sub-fail"
                elif "🧪" in heading_text or "EXPERIMENTAL" in heading_text:
                    status_class = "sub-exp"
                
                html_lines.append(f'<h3 class="subsection-title {status_class}">{format_inline(heading_text)}</h3>')
            elif level == 4:
                html_lines.append(f'<h4 class="card-title">{format_inline(heading_text)}</h4>')
            i += 1
            continue

        # Handle Blockquotes / Callout Alerts
        if stripped.startswith(">"):
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            quote_text = stripped[1:].strip()
            while i + 1 < len(lines) and lines[i+1].strip().startswith(">"):
                i += 1
                quote_text += " " + lines[i].strip()[1:].strip()
            html_lines.append(f'<div class="callout"><div class="callout-icon">ℹ️</div><div class="callout-body">{format_inline(quote_text)}</div></div>')
            i += 1
            continue

        # Handle Lists
        list_match = re.match(r'^(\*|-|\+)\s+(.+)', stripped)
        num_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if list_match or num_match:
            current_tag = "ol" if num_match else "ul"
            item_text = num_match.group(2) if num_match else list_match.group(2)
            
            if not in_list:
                in_list = True
                list_tag = current_tag
                html_lines.append(f"<{list_tag}>")
            elif in_list and list_tag != current_tag:
                html_lines.append(f"</{list_tag}>")
                list_tag = current_tag
                html_lines.append(f"<{list_tag}>")

            html_lines.append(f"<li>{format_inline(item_text)}</li>")
            i += 1
            continue
        elif in_list:
            html_lines.append(f"</{list_tag}>")
            in_list = False

        # Regular Paragraph
        if stripped:
            if stripped.startswith("**Target") or stripped.startswith("**Audit Date") or stripped.startswith("**Site Classification") or stripped.startswith("**Overall Readiness"):
                html_lines.append(f'<p class="meta-line">{format_inline(stripped)}</p>')
            else:
                html_lines.append(f'<p>{format_inline(stripped)}</p>')

        i += 1

    if in_table:
        html_lines.append(flush_table())
    if in_list:
        html_lines.append(f"</{list_tag}>")

    body_html = "\n".join(html_lines)

    full_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{html.escape(title)}</title>
<style>
:root {{
    --bg-main: #ffffff;
    --text-main: #0f172a;
    --text-muted: #475569;
    --text-light: #64748b;
    --border-color: #e2e8f0;
    --border-subtle: #f1f5f9;
    --primary-color: #2563eb;
    --primary-dark: #1d4ed8;
    --code-bg: #0f172a;
    --code-text: #e2e8f0;
    --card-bg: #f8fafc;
}}

@page {{
    size: A4 portrait;
    margin: 14mm 12mm 14mm 12mm;
    @top-left {{
        content: "AI Visibility Audit Report";
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #94a3b8;
        font-weight: 500;
    }}
    @top-right {{
        content: "Verified Audit Standard";
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #94a3b8;
        font-weight: 500;
    }}
    @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }}
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: var(--text-main);
    background: var(--bg-main);
    line-height: 1.48;
    font-size: 9pt;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

.report-wrapper {{
    max-width: 100%;
    margin: 0 auto;
}}

/* Header Styling */
.doc-header {{
    border-bottom: 2.5px solid #2563eb;
    padding-bottom: 10px;
    margin-bottom: 12px;
}}

.brand-pill {{
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #2563eb;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 5px;
}}

.doc-title {{
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

/* Section Titles */
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 16px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border-color);
    page-break-after: avoid;
    break-after: avoid;
}}

.subsection-title {{
    font-size: 10pt;
    font-weight: 600;
    color: #334155;
    margin-top: 13px;
    margin-bottom: 5px;
    padding-left: 6px;
    border-left: 3px solid #cbd5e1;
    page-break-after: avoid;
    break-after: avoid;
}}

.subsection-title.sub-pass {{
    border-left-color: #10b981;
    color: #065f46;
}}

.subsection-title.sub-warn {{
    border-left-color: #f59e0b;
    color: #92400e;
}}

.subsection-title.sub-fail {{
    border-left-color: #ef4444;
    color: #991b1b;
}}

.subsection-title.sub-exp {{
    border-left-color: #8b5cf6;
    color: #5b21b6;
}}

.card-title {{
    font-size: 9.5pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 8px;
    margin-bottom: 3px;
}}

p {{
    margin-bottom: 6px;
    color: var(--text-main);
}}

.meta-line {{
    font-size: 8.5pt;
    color: #334155;
    margin-bottom: 3px;
}}

.divider {{
    border: 0;
    height: 1px;
    background: var(--border-color);
    margin: 12px 0;
}}

/* Scorecard Gauges */
.score-gauge-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7px;
    margin: 10px 0 14px 0;
}}

.score-card {{
    border: 1px solid var(--border-color);
    border-radius: 7px;
    padding: 8px 4px 6px 4px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.gauge-container {{
    position: relative;
    width: 52px;
    height: 52px;
    margin: 0 auto;
}}

.gauge-svg {{
    width: 52px;
    height: 52px;
    transform: rotate(-90deg);
}}

.gauge-bg {{
    fill: none;
    stroke: #e2e8f0;
    stroke-width: 4.5;
}}

.gauge-fill {{
    fill: none;
    stroke-width: 4.8;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.3s ease;
}}

.gauge-score {{
    position: absolute;
    top: 0;
    left: 0;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10pt;
    font-weight: 800;
    letter-spacing: -0.04em;
}}

.gauge-label {{
    font-size: 7.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 5px;
    line-height: 1.15;
    min-height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.gauge-status {{
    margin-top: 3px;
}}

/* Tables */
.table-container {{
    margin: 8px 0 12px 0;
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    text-align: left;
}}

th {{
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 600;
    padding: 5px 7px;
    border: 1px solid #cbd5e1;
    font-size: 7.5pt;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}

td {{
    padding: 5px 7px;
    border: 1px solid var(--border-color);
    color: #334155;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: #f8fafc;
}}

/* Badges */
.badge {{
    display: inline-block;
    font-size: 6.5pt;
    font-weight: 700;
    padding: 1.5px 5px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    white-space: nowrap;
}}

.badge-critical {{ background: #ffe4e6; color: #be123c; border: 1px solid #fecdd3; }}
.badge-high {{ background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }}
.badge-medium {{ background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }}
.badge-low {{ background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }}

.badge-pass {{ background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }}
.badge-fail {{ background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }}
.badge-ready {{ background: #dcfce7; color: #166534; border: 1px solid #86efac; }}
.badge-partial {{ background: #fef9c3; color: #854d0e; border: 1px solid #fde047; }}
.badge-blocked {{ background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }}
.badge-exp {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #d8b4fe; font-size: 6pt; }}

/* Code Blocks */
.code-block {{
    background: var(--code-bg);
    border-radius: 5px;
    margin: 6px 0 9px 0;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

.code-header {{
    background: #1e293b;
    padding: 3px 7px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #334155;
}}

.code-dot {{
    width: 5px;
    height: 5px;
    border-radius: 50%;
    margin-right: 3px;
}}
.dot-red {{ background: #ef4444; }}
.dot-yellow {{ background: #f59e0b; }}
.dot-green {{ background: #10b981; }}

.code-lang {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 6pt;
    color: #94a3b8;
    margin-left: auto;
    text-transform: uppercase;
}}

pre {{
    padding: 6px 8px;
    overflow-x: auto;
    margin: 0;
}}

code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    color: var(--code-text);
    line-height: 1.38;
}}

p code, li code, td code {{
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 3px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
    font-size: 7.5pt;
    font-weight: 500;
}}

/* Callouts */
.callout {{
    background: #f8fafc;
    border-left: 3.5px solid #3b82f6;
    padding: 6px 8px;
    border-radius: 0 5px 5px 0;
    margin: 8px 0 10px 0;
    display: flex;
    align-items: flex-start;
}}

.callout-icon {{
    font-size: 10pt;
    margin-right: 5px;
    line-height: 1;
}}

.callout-body {{
    font-size: 8pt;
    color: #334155;
    flex: 1;
}}

/* Lists */
ul, ol {{
    margin: 5px 0 9px 16px;
    color: #334155;
    font-size: 8.5pt;
}}

li {{
    margin-bottom: 2.5px;
}}

a {{
    color: #2563eb;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

/* Page Break Control */
.avoid-break {{
    page-break-inside: avoid;
    break-inside: avoid;
}}
</style>
</head>
<body>
<div class="report-wrapper">
{body_html}
</div>
</body>
</html>
"""
    return full_document


def render_pdf(html_path: str, pdf_path: str, browser_path: str) -> bool:
    """Executes headless Chrome/Edge to render the HTML document to PDF."""
    # Ensure target directory exists
    Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        browser_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={str(pdf_path)}",
        str(html_path)
    ]
    try:
        res = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )
        return os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 0
    except Exception as e:
        print(f"Error executing browser PDF export: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python render-audit-pdf.py <input_report.md> [output_report.pdf]")
        sys.exit(1)

    input_md_path = Path(sys.argv[1]).resolve()
    if not input_md_path.is_file():
        print(f"Error: File not found: {input_md_path}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_pdf_path = Path(sys.argv[2]).resolve()
    else:
        output_pdf_path = input_md_path.with_suffix(".pdf")

    output_html_path = input_md_path.with_suffix(".html")

    md_content = input_md_path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else input_md_path.stem

    # 1. Render HTML
    html_content = markdown_to_html(md_content, title=title)
    output_html_path.write_text(html_content, encoding="utf-8")
    print(f"[OK] Generated HTML report: {output_html_path}")

    # 2. Render PDF using Chromium/Chrome/Edge
    browser_exe = find_browser_executable()
    if not browser_exe:
        print("[WARNING] No local Chrome/Edge executable found. PDF generation skipped. HTML report is ready.")
        sys.exit(0)

    print(f"Using browser: {browser_exe}")
    success = render_pdf(str(output_html_path), str(output_pdf_path), browser_exe)

    if success:
        print(f"[OK] Generated PDF report: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    else:
        print(f"[ERROR] Failed to generate PDF with {browser_exe}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

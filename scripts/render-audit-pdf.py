#!/usr/bin/env python3
"""render-audit-pdf.py

Transforms an AI Visibility audit Markdown document (v1, v2, or v3 format) into a
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
    # Clean score: strip [82](url) or [82] or `82` or *82*
    score_clean = re.sub(r'\[([^\]]+)\](?:\([^)]+\))?', r'\1', raw_score).strip()
    score_clean = re.sub(r'[\[\]`*]', '', score_clean).strip()

    label_clean = re.sub(r'\[([^\]]+)\](?:\([^)]+\))?', r'\1', label_text).strip()
    label_clean = re.sub(r'[*`]', '', label_clean).strip()

    status_clean = re.sub(r'\[([^\]]+)\](?:\([^)]+\))?', r'\1', status_text).strip()
    status_clean = re.sub(r'[*`]', '', status_clean).strip()

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
    if any(k in status_clean.upper() for k in ["PASS", "READY", "100", "✅", "YES"]):
        badge_class = "badge-pass"
    elif any(k in status_clean.upper() for k in ["FAIL", "BLOCKED", "0", "❌", "NO"]):
        badge_class = "badge-fail"
    elif any(k in status_clean.upper() for k in ["PARTIAL", "WARN", "⚠️", "IMPROVE"]):
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
    in_finding_card = False
    in_exec_box = False
    in_exec_2col_grid = False

    def close_containers():
        nonlocal in_finding_card, in_exec_box, in_exec_2col_grid, in_list, list_tag
        if in_list:
            html_lines.append(f"</{list_tag}>")
            in_list = False
        if in_finding_card:
            html_lines.append('</div>')
            in_finding_card = False
        if in_exec_box:
            html_lines.append('</div>')
            in_exec_box = False
        if in_exec_2col_grid:
            html_lines.append('</div>')
            in_exec_2col_grid = False

    def format_inline(text: str) -> str:
        text = html.escape(text)
        
        # Replace status badges (supporting emojis, tiers, priorities, and v1/v2/v3 tokens)
        text = re.sub(r'`(✅\s*YES|YES)`', r'<span class="badge badge-pass">✅ YES</span>', text, flags=re.I)
        text = re.sub(r'`(⚠️\s*PARTIAL|PARTIAL)`', r'<span class="badge badge-partial">⚠️ PARTIAL</span>', text, flags=re.I)
        text = re.sub(r'`(❌\s*NO|NO)`', r'<span class="badge badge-fail">❌ NO</span>', text, flags=re.I)
        text = re.sub(r'`(✅\s*PASS|PASS)`', r'<span class="badge badge-pass">✅ PASS</span>', text, flags=re.I)
        text = re.sub(r'`(⚠️\s*(?:WARN|PARTIAL)|PARTIALLY\s*READY|WARN|PARTIAL|NEEDS\s*IMPROVEMENT)`', r'<span class="badge badge-partial">⚠️ WARN</span>', text, flags=re.I)
        text = re.sub(r'`(❌\s*(?:FAIL|CRITICAL)|FAIL|CRITICAL|BLOCKED)`', r'<span class="badge badge-fail">❌ FAIL</span>', text, flags=re.I)
        text = re.sub(r'`(READY)`', r'<span class="badge badge-ready">READY</span>', text, flags=re.I)

        # Priorities
        text = re.sub(r'`(P0(?:\s*\(Immediate\))?|P0\s*-\s*DO\s*NOW|P0\s*DO\s*NOW)`', r'<span class="badge badge-p0">P0 DO NOW</span>', text, flags=re.I)
        text = re.sub(r'`(P1(?:\s*\(Next\))?|P1\s*-\s*DO\s*NEXT|P1\s*DO\s*NEXT)`', r'<span class="badge badge-p1">P1 DO NEXT</span>', text, flags=re.I)
        text = re.sub(r'`(P2(?:\s*\(Improve\))?|P2\s*-\s*IMPROVE|P2\s*IMPROVE)`', r'<span class="badge badge-p2">P2 IMPROVE</span>', text, flags=re.I)
        text = re.sub(r'`(P3(?:\s*\(Optional\))?|P3\s*-\s*OPTIONAL|P3\s*OPTIONAL)`', r'<span class="badge badge-p3">P3 OPTIONAL</span>', text, flags=re.I)

        # Severities
        text = re.sub(r'`(HIGH)`', r'<span class="badge badge-high">HIGH</span>', text, flags=re.I)
        text = re.sub(r'`(MEDIUM)`', r'<span class="badge badge-medium">MEDIUM</span>', text, flags=re.I)
        text = re.sub(r'`(LOW)`', r'<span class="badge badge-low">LOW</span>', text, flags=re.I)

        # Evidence Tiers
        text = re.sub(r'`(CRITICAL\s*FOUNDATION|CRITICAL)`', r'<span class="badge badge-tier-critical">CRITICAL FOUNDATION</span>', text, flags=re.I)
        text = re.sub(r'`(IMPORTANT\s*IMPROVEMENT|IMPORTANT)`', r'<span class="badge badge-tier-important">IMPORTANT IMPROVEMENT</span>', text, flags=re.I)
        text = re.sub(r'`(SUPPORTING\s*SIGNAL|SUPPORTING)`', r'<span class="badge badge-tier-supporting">SUPPORTING SIGNAL</span>', text, flags=re.I)
        text = re.sub(r'`(EXPERIMENTAL\s*PROTOCOL|EXPERIMENTAL|🧪\s*EXPERIMENTAL|🧪\s*DRAFT|OPTIONAL\s*\(DRAFT\)|DRAFT\s*PROTOCOLS)`', r'<span class="badge badge-exp">🧪 EXPERIMENTAL</span>', text, flags=re.I)
        text = re.sub(r'\[EXPERIMENTAL\]', r'<span class="badge badge-exp">EXPERIMENTAL</span>', text)

        # Confidence Levels
        text = re.sub(r'`(High\s*\[Measured\]|HIGH\s*-\s*MEASURED)`', r'<span class="badge badge-conf-high">HIGH [MEASURED]</span>', text, flags=re.I)
        text = re.sub(r'`(High\s*\[Derived\]|HIGH\s*-\s*DERIVED)`', r'<span class="badge badge-conf-high">HIGH [DERIVED]</span>', text, flags=re.I)
        text = re.sub(r'`(Medium\s*\[Derived\]|MEDIUM\s*-\s*DERIVED)`', r'<span class="badge badge-conf-med">MEDIUM [DERIVED]</span>', text, flags=re.I)
        text = re.sub(r'`(Low\s*\[Estimated\]|LOW\s*-\s*ESTIMATED)`', r'<span class="badge badge-conf-low">LOW [ESTIMATED]</span>', text, flags=re.I)
        
        # Inline code - high contrast dark text
        text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
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

        # Check if this table is a Scorecard Gauge Table:
        header_raw_cols = [c.strip() for c in rows[0].strip('|').split('|')]
        is_scorecard = len(header_raw_cols) >= 1 and any(
            re.search(r'(\[\d+\]|\b\d{1,3}\b|\b\d/\d\b)', c) for c in header_raw_cols
        ) and len(rows) >= 3

        if is_scorecard:
            scores = header_raw_cols
            labels = [c.strip() for c in rows[2].strip('|').split('|')] if len(rows) > 2 else [""] * len(scores)
            statuses = [c.strip() for c in rows[3].strip('|').split('|')] if len(rows) > 3 else [""] * len(scores)

            num_cols = len(scores)
            grid_class = f"score-gauge-grid cols-{num_cols}" if num_cols in [4, 6, 8] else "score-gauge-grid"
            out = [f'<div class="{grid_class} avoid-break">']
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
                # Center align checkmark/status-like short cells
                is_short_center = len(col.strip()) <= 14 and any(sym in col for sym in ["✅", "⚠️", "❌", "PASS", "WARN", "FAIL", "YES", "NO", "P0", "P1", "P2", "P3"])
                td_attr = ' class="text-center"' if is_short_center else ''
                out.append(f'<td{td_attr}>{format_inline(col)}</td>')
            out.append('</tr>')

        out.append('</tbody></table></div>')
        in_table = False
        table_buffer = []
        return '\n'.join(out)

    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Handle HTML Comments & Page Breaks
        if stripped.startswith("<!--") and "PAGE BREAK" in stripped.upper():
            close_containers()
            if in_table:
                html_lines.append(flush_table())
            html_lines.append('<div class="page-break"></div>')
            i += 1
            continue

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
            close_containers()
            html_lines.append('<hr class="divider"/>')
            i += 1
            continue

        # Handle Headings
        if stripped.startswith("#"):
            level = len(re.match(r'^(#+)', stripped).group(1))
            heading_text = stripped[level:].strip()
            
            if level == 1:
                close_containers()
                html_lines.append(f'''
                <div class="doc-header">
                    <div class="doc-header-top">
                        <div class="brand-pill">AI Visibility & Readiness Audit</div>
                        <div class="doc-badge-verified">Verified Audit Architecture</div>
                    </div>
                    <h1 class="doc-title">{format_inline(heading_text)}</h1>
                </div>''')
            elif level == 2:
                close_containers()
                html_lines.append(f'<h2 class="section-title">{format_inline(heading_text)}</h2>')
            elif level == 3:
                close_containers()
                status_class = ""
                if "✅" in heading_text or "PASS" in heading_text:
                    status_class = "sub-pass"
                elif "⚠️" in heading_text or "WARN" in heading_text or "PARTIAL" in heading_text:
                    status_class = "sub-warn"
                elif "❌" in heading_text or "FAIL" in heading_text:
                    status_class = "sub-fail"
                elif "🧪" in heading_text or "EXPERIMENTAL" in heading_text:
                    status_class = "sub-exp"
                elif "PILLAR" in heading_text.upper():
                    status_class = "sub-pillar"
                elif "TICKET" in heading_text.upper():
                    status_class = "sub-ticket"
                
                if "BRIEFING" in heading_text.upper():
                    in_exec_box = True
                    html_lines.append(f'<div class="exec-briefing-box avoid-break"><h4 class="briefing-title">{format_inline(heading_text)}</h4>')
                else:
                    html_lines.append(f'<h3 class="subsection-title {status_class}">{format_inline(heading_text)}</h3>')
            elif level == 4:
                if "FINDING" in heading_text.upper():
                    close_containers()
                    in_finding_card = True
                    html_lines.append(f'<div class="finding-card avoid-break"><h4 class="card-title">{format_inline(heading_text)}</h4>')
                elif any(sym in heading_text for sym in ["🟢", "What Is Working"]):
                    close_containers()
                    in_exec_2col_grid = True
                    in_exec_box = True
                    html_lines.append('<div class="exec-2col-row avoid-break">')
                    html_lines.append(f'<div class="exec-box box-strengths"><h4 class="exec-box-title">{format_inline(heading_text)}</h4>')
                elif any(sym in heading_text for sym in ["🔴", "What Is Limiting"]):
                    if in_list:
                        html_lines.append(f"</{list_tag}>")
                        in_list = False
                    if in_exec_box:
                        html_lines.append('</div>')
                        in_exec_box = False
                    in_exec_box = True
                    html_lines.append(f'<div class="exec-box box-limitations"><h4 class="exec-box-title">{format_inline(heading_text)}</h4>')
                elif any(sym in heading_text for sym in ["🎯", "Top 3", "Priority Actions"]):
                    close_containers()
                    in_exec_box = True
                    html_lines.append(f'<div class="exec-box box-actions avoid-break"><h4 class="exec-box-title">{format_inline(heading_text)}</h4>')
                else:
                    close_containers()
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

        # Handle Checklist items: - [ ] or - [x]
        check_match = re.match(r'^(?:\*|-|\+)\s+\[([ xX])\]\s+(.+)', stripped)
        if check_match:
            is_checked = check_match.group(1).lower() == 'x'
            check_text = check_match.group(2)
            check_icon = "☑️" if is_checked else "⬜"
            check_class = "check-done" if is_checked else "check-todo"
            
            if not in_list:
                in_list = True
                list_tag = "ul"
                html_lines.append(f'<ul class="checklist">')
            
            html_lines.append(f'<li class="{check_class}"><span class="check-icon">{check_icon}</span> {format_inline(check_text)}</li>')
            i += 1
            continue

        # Handle Regular Lists
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

    close_containers()
    if in_table:
        html_lines.append(flush_table())

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
    margin: 10mm 10mm 10mm 10mm;
    @top-left {{
        content: "AI Visibility & Website Readiness Audit";
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
        color: #94a3b8;
        font-weight: 500;
    }}
    @top-right {{
        content: "V3 Decision Architecture";
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
        color: #94a3b8;
        font-weight: 500;
    }}
    @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
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
    line-height: 1.42;
    font-size: 8.5pt;
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
    border-bottom: 2px solid #2563eb;
    padding-bottom: 6px;
    margin-bottom: 8px;
}}

.doc-header-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3px;
}}

.brand-pill {{
    display: inline-block;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #2563eb;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 1.5px 7px;
    border-radius: 4px;
}}

.doc-badge-verified {{
    font-size: 6.8pt;
    font-weight: 700;
    color: #047857;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 1.5px 7px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

.doc-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    line-height: 1.18;
    margin-top: 2px;
}}

/* Section Titles */
.section-title {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 10px;
    margin-bottom: 5px;
    padding-bottom: 2.5px;
    border-bottom: 1.5px solid var(--border-color);
    page-break-after: avoid;
    break-after: avoid;
}}

.subsection-title {{
    font-size: 9pt;
    font-weight: 600;
    color: #334155;
    margin-top: 8px;
    margin-bottom: 3px;
    padding-left: 5px;
    border-left: 3px solid #cbd5e1;
    page-break-after: avoid;
    break-after: avoid;
}}

.subsection-title.sub-pass {{ border-left-color: #10b981; color: #065f46; }}
.subsection-title.sub-warn {{ border-left-color: #f59e0b; color: #92400e; }}
.subsection-title.sub-fail {{ border-left-color: #ef4444; color: #991b1b; }}
.subsection-title.sub-exp {{ border-left-color: #8b5cf6; color: #5b21b6; }}
.subsection-title.sub-pillar {{ border-left-color: #2563eb; color: #1e40af; background: #eff6ff; padding: 2.5px 6px; border-radius: 0 4px 4px 0; }}
.subsection-title.sub-ticket {{ border-left-color: #0284c7; color: #0369a1; background: #f0f9ff; padding: 2.5px 6px; border-radius: 0 4px 4px 0; }}

.card-title {{
    font-size: 8.8pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 2px;
    margin-bottom: 2px;
}}

p {{
    margin-bottom: 3.5px;
    color: var(--text-main);
}}

.meta-line {{
    font-size: 8pt;
    color: #334155;
    margin-bottom: 2px;
}}

.divider {{
    border: 0;
    height: 1px;
    background: var(--border-color);
    margin: 8px 0;
}}

/* Scorecard Gauges */
.score-gauge-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    margin: 6px 0 8px 0;
}}

.score-gauge-grid.cols-6 {{
    grid-template-columns: repeat(6, 1fr);
    gap: 4px;
}}

.score-gauge-grid.cols-8 {{
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
}}

.score-card {{
    border: 1px solid var(--border-color);
    border-radius: 5px;
    padding: 5px 2px 3px 2px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.gauge-container {{
    position: relative;
    width: 42px;
    height: 42px;
    margin: 0 auto;
}}

.gauge-svg {{
    width: 42px;
    height: 42px;
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
}}

.gauge-score {{
    position: absolute;
    top: 0;
    left: 0;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', -apple-system, sans-serif;
    font-size: 9pt;
    font-weight: 800;
    letter-spacing: -0.04em;
}}

.gauge-label {{
    font-size: 6.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 2px;
    line-height: 1.1;
    min-height: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.gauge-status {{
    margin-top: 1px;
}}

/* Executive Overview Layout (2-Column Grid for Strengths & Limitations) */
.exec-2col-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin: 4px 0 6px 0;
    page-break-inside: avoid;
    break-inside: avoid;
}}

.exec-box {{
    border-radius: 5px;
    padding: 5px 8px;
    margin: 4px 0 6px 0;
    border-left: 3.5px solid #cbd5e1;
    box-sizing: border-box;
}}

.exec-2col-row .exec-box {{
    margin: 0;
    height: 100%;
}}

.exec-box.box-strengths {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3.5px solid #10b981; }}
.exec-box.box-limitations {{ background: #fef2f2; border: 1px solid #fecaca; border-left: 3.5px solid #ef4444; }}
.exec-box.box-actions {{ background: #eff6ff; border: 1px solid #bfdbfe; border-left: 3.5px solid #2563eb; }}

.exec-box-title {{
    font-size: 8.5pt;
    font-weight: 700;
    margin-bottom: 2px;
    color: #0f172a;
}}

.exec-box ul, .exec-box ol {{
    margin: 2px 0 2px 14px;
    padding: 0;
}}

.exec-box li {{
    margin-bottom: 1.5px;
    font-size: 7.8pt;
    line-height: 1.35;
}}

/* Briefing Box */
.exec-briefing-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #475569;
    border-radius: 5px;
    padding: 5px 8px;
    margin: 4px 0 6px 0;
}}

.briefing-title {{
    font-size: 8.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 2px;
}}

.exec-briefing-box ul {{
    margin: 2px 0 2px 14px;
    padding: 0;
}}

.exec-briefing-box li {{
    margin-bottom: 1.5px;
    font-size: 7.8pt;
    color: #334155;
    line-height: 1.35;
}}

/* Finding Cards */
.finding-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 3.5px solid #3b82f6;
    border-radius: 5px;
    padding: 6px 8px;
    margin: 6px 0 8px 0;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}}

/* Tables */
.table-container {{
    margin: 5px 0 8px 0;
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.5pt;
    text-align: left;
}}

th {{
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 600;
    padding: 3.5px 5px;
    border: 1px solid #cbd5e1;
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}

td {{
    padding: 3.5px 5px;
    border: 1px solid var(--border-color);
    color: #334155;
    vertical-align: top;
}}

td.text-center {{
    text-align: center;
}}

tr:nth-child(even) td {{
    background: #f8fafc;
}}

/* Badges */
.badge {{
    display: inline-block;
    font-size: 6.2pt;
    font-weight: 700;
    padding: 1px 4px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    white-space: nowrap;
}}

.badge-critical {{ background: #ffe4e6; color: #be123c; border: 1px solid #fecdd3; }}
.badge-high {{ background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }}
.badge-medium {{ background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }}
.badge-low {{ background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }}

/* Priorities */
.badge-p0 {{ background: #fee2e2; color: #991b1b; border: 1px solid #f87171; font-weight: 800; }}
.badge-p1 {{ background: #ffedd5; color: #c2410c; border: 1px solid #fb923c; font-weight: 800; }}
.badge-p2 {{ background: #fef3c7; color: #b45309; border: 1px solid #facc15; font-weight: 700; }}
.badge-p3 {{ background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; font-weight: 600; }}

/* Evidence Tiers */
.badge-tier-critical {{ background: #ffe4e6; color: #9f1239; border: 1px solid #fda4af; font-size: 5.8pt; }}
.badge-tier-important {{ background: #ffedd5; color: #9a3412; border: 1px solid #fdba74; font-size: 5.8pt; }}
.badge-tier-supporting {{ background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; font-size: 5.8pt; }}

/* Confidence */
.badge-conf-high {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; font-size: 5.8pt; }}
.badge-conf-med {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; font-size: 5.8pt; }}
.badge-conf-low {{ background: #f8fafc; color: #64748b; border: 1px solid #e2e8f0; font-size: 5.8pt; }}

.badge-pass {{ background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }}
.badge-fail {{ background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }}
.badge-ready {{ background: #dcfce7; color: #166534; border: 1px solid #86efac; }}
.badge-partial {{ background: #fef9c3; color: #854d0e; border: 1px solid #fde047; }}
.badge-blocked {{ background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }}
.badge-exp {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #d8b4fe; font-size: 5.8pt; }}

/* High-Contrast Code Elements */
code {{
    font-family: 'JetBrains Mono', -apple-system, monospace;
    font-size: 7.2pt;
    color: #0f172a !important;
    background: #e2e8f0;
    padding: 1px 3px;
    border-radius: 3px;
    border: 1px solid #cbd5e1;
    font-weight: 600;
}}

.inline-code {{
    color: #0f172a !important;
    background: #e2e8f0;
    border: 1px solid #cbd5e1;
}}

/* Code Blocks */
.code-block {{
    background: var(--code-bg);
    border-radius: 5px;
    margin: 4px 0 6px 0;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

.code-header {{
    background: #1e293b;
    padding: 3px 6px;
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
    font-size: 5.8pt;
    color: #94a3b8;
    margin-left: auto;
    text-transform: uppercase;
}}

pre {{
    padding: 4px 6px;
    overflow-x: auto;
    margin: 0;
}}

pre code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    color: var(--code-text) !important;
    background: transparent;
    padding: 0;
    border: none;
    font-weight: 400;
    line-height: 1.32;
}}

/* Callouts */
.callout {{
    background: #f8fafc;
    border-left: 3.5px solid #3b82f6;
    padding: 5px 7px;
    border-radius: 0 5px 5px 0;
    margin: 5px 0 7px 0;
    display: flex;
    align-items: flex-start;
}}

.callout-icon {{
    font-size: 9pt;
    margin-right: 5px;
    line-height: 1;
}}

.callout-body {{
    font-size: 7.5pt;
    color: #334155;
    flex: 1;
}}

.callout-body code {{
    background: #e2e8f0;
    color: #0f172a !important;
    border: 1px solid #cbd5e1;
    font-weight: 700;
}}

/* Lists */
ul, ol {{
    margin: 3px 0 6px 14px;
    color: #334155;
    font-size: 7.8pt;
}}

li {{
    margin-bottom: 1.5px;
}}

ul.checklist {{
    list-style: none;
    margin-left: 2px;
}}

ul.checklist li {{
    display: flex;
    align-items: center;
    margin-bottom: 1.5px;
}}

.check-icon {{
    font-size: 7pt;
    margin-right: 4px;
}}

a {{
    color: #2563eb;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

/* Page Break Control */
.page-break {{
    page-break-after: always;
    break-after: page;
    height: 0;
    margin: 0;
    padding: 0;
}}

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


def render_pdf(html_path: str, pdf_path: str, browser_path: str) -> tuple[bool, str]:
    """Executes headless Chrome/Edge to render the HTML document to PDF.
    
    Returns (success, actual_pdf_path).
    """
    target_path = Path(pdf_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if target file is locked by Adobe Reader / other processes
    if target_path.exists():
        try:
            target_path.unlink()
        except (PermissionError, OSError):
            fallback_name = f"{target_path.stem}_latest{target_path.suffix}"
            target_path = target_path.with_name(fallback_name)
            if target_path.exists():
                try:
                    target_path.unlink()
                except Exception:
                    pass

    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={str(target_path)}",
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
        is_ok = target_path.is_file() and target_path.stat().st_size > 0
        return is_ok, str(target_path)
    except Exception as e:
        print(f"Error executing browser PDF export: {e}", file=sys.stderr)
        return False, str(target_path)


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
    success, actual_pdf = render_pdf(str(output_html_path), str(output_pdf_path), browser_exe)

    if success:
        print(f"[OK] Generated PDF report: {actual_pdf} ({os.path.getsize(actual_pdf)} bytes)")
    else:
        print(f"[ERROR] Failed to generate PDF with {browser_exe}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

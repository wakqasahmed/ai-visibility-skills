#!/usr/bin/env python3
"""render-audit-pdf.py

Transforms an AI Visibility audit Markdown document into a beautifully styled,
executive HTML document and renders it into a print-perfect PDF using a local
headless Chromium-based browser (Chrome, Edge, or Chromium).

Zero external pip dependencies required. Uses Python standard library + local browser.

Usage:
    python scripts/render-audit-pdf.py path/to/audit_report.md [path/to/output.pdf]
"""

import os
import sys
import re
import html
import subprocess
import shutil
from pathlib import Path


def find_browser_executable() -> str | None:
    """Find a local Chrome, Edge, or Chromium browser executable."""
    candidates = []

    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        candidates.extend([
            os.path.join(prog_files, "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(prog_files_x86, "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(prog_files_x86, "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(prog_files, "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(local_app, "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(local_app, "Microsoft\\Edge\\Application\\msedge.exe"),
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

        out = ['<div class="table-container"><table>']
        # Header row
        header_cols = [c.strip() for c in rows[0].strip('|').split('|')]
        out.append('<thead><tr>')
        for col in header_cols:
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

    def format_inline(text: str) -> str:
        # Badges & labels
        text = html.escape(text)
        
        # Restore intentional bold and code markers
        # Replace status badges
        text = re.sub(r'`CRITICAL`', r'<span class="badge badge-critical">CRITICAL</span>', text, flags=re.I)
        text = re.sub(r'`HIGH`', r'<span class="badge badge-high">HIGH</span>', text, flags=re.I)
        text = re.sub(r'`MEDIUM`', r'<span class="badge badge-medium">MEDIUM</span>', text, flags=re.I)
        text = re.sub(r'`LOW`', r'<span class="badge badge-low">LOW</span>', text, flags=re.I)
        text = re.sub(r'`PASS`', r'<span class="badge badge-pass">PASS</span>', text, flags=re.I)
        text = re.sub(r'`FAIL`', r'<span class="badge badge-fail">FAIL</span>', text, flags=re.I)
        text = re.sub(r'`READY`', r'<span class="badge badge-ready">READY</span>', text, flags=re.I)
        text = re.sub(r'`PARTIALLY READY`', r'<span class="badge badge-partial">PARTIALLY READY</span>', text, flags=re.I)
        text = re.sub(r'`BLOCKED`', r'<span class="badge badge-blocked">BLOCKED</span>', text, flags=re.I)
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
                html_lines.append(f'<h3 class="subsection-title">{format_inline(heading_text)}</h3>')
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
            # gather following lines if part of same quote
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
            # Check for metadata lines like **Target Domain:**
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

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
    margin: 16mm 14mm 16mm 14mm;
    @top-left {{
        content: "AI Visibility Audit Report";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
        font-weight: 500;
    }}
    @top-right {{
        content: "Verified Audit Standard";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
        font-weight: 500;
    }}
    @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'Inter', sans-serif;
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
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: var(--text-main);
    background: var(--bg-main);
    line-height: 1.55;
    font-size: 10pt;
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
    padding-bottom: 12px;
    margin-bottom: 16px;
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
    margin-bottom: 6px;
}}

.doc-title {{
    font-size: 19pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

/* Section Titles */
.section-title {{
    font-size: 13pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 20px;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border-color);
    page-break-after: avoid;
    break-after: avoid;
}}

.subsection-title {{
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
}}

.card-title {{
    font-size: 10.5pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 10px;
    margin-bottom: 4px;
}}

p {{
    margin-bottom: 8px;
    color: var(--text-main);
}}

.meta-line {{
    font-size: 9.5pt;
    color: #334155;
    margin-bottom: 4px;
}}

.divider {{
    border: 0;
    height: 1px;
    background: var(--border-color);
    margin: 16px 0;
}}

/* Tables */
.table-container {{
    margin: 12px 0 16px 0;
    overflow-x: auto;
    page-break-inside: avoid;
    break-inside: avoid;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    text-align: left;
}}

th {{
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 600;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}

td {{
    padding: 7px 10px;
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
    font-size: 7.5pt;
    font-weight: 700;
    padding: 2px 7px;
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
.badge-exp {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #d8b4fe; font-size: 7pt; }}

/* Code Blocks */
.code-block {{
    background: var(--code-bg);
    border-radius: 6px;
    margin: 10px 0 14px 0;
    overflow: hidden;
    page-break-inside: avoid;
    break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

.code-header {{
    background: #1e293b;
    padding: 4px 10px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #334155;
}}

.code-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    margin-right: 4px;
}}
.dot-red {{ background: #ef4444; }}
.dot-yellow {{ background: #f59e0b; }}
.dot-green {{ background: #10b981; }}

.code-lang {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    color: #94a3b8;
    margin-left: auto;
    text-transform: uppercase;
}}

pre {{
    padding: 10px 12px;
    overflow-x: auto;
    margin: 0;
}}

code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    color: var(--code-text);
    line-height: 1.45;
}}

p code, li code, td code {{
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
    font-size: 8.5pt;
    font-weight: 500;
}}

/* Callouts */
.callout {{
    background: #f8fafc;
    border-left: 3.5px solid #3b82f6;
    padding: 10px 12px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 16px 0;
    display: flex;
    align-items: flex-start;
    page-break-inside: avoid;
    break-inside: avoid;
}}

.callout-icon {{
    font-size: 12pt;
    margin-right: 8px;
    line-height: 1;
}}

.callout-body {{
    font-size: 9pt;
    color: #334155;
    flex: 1;
}}

/* Lists */
ul, ol {{
    margin: 8px 0 12px 20px;
    color: #334155;
    font-size: 9.5pt;
}}

li {{
    margin-bottom: 4px;
}}

a {{
    color: #2563eb;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

/* Page Break Helpers */
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
    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
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

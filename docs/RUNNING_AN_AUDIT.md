# Running an audit on your own machine

This walks through installing this pack and running a real skill against a real site, from your own terminal — no sandboxed dev environment assumed.

## 1. Prerequisites

- An AI coding agent that supports Agent Skills and can run shell commands (e.g., Claude Code, Antigravity, Cursor, Codex; other Agent-Skills-compatible agents work the same way).
- Either `node`/`npx` available, or just `git` — both install paths below work; the git path needs no Node.

## 2. Install the skill pack

Pick one, from your terminal:

**Via npx (simplest):**

```bash
npx skills@latest add wakqasahmed/ai-visibility-skills
```

Installs all 10 skills into wherever your agent looks for skills (Claude Code: `.claude/skills/` in the current project; Antigravity: `.agents/skills/`; add `-g` to install once for every project instead of per-project).

**Just one skill** — e.g. the crawler-access check:

```bash
npx skills@latest add wakqasahmed/ai-visibility-skills --skill robots-ai-crawler-audit
```

**No Node available — git clone:**

```bash
git clone https://github.com/wakqasahmed/ai-visibility-skills.git
cp -r ai-visibility-skills/skills/ai-visibility/* .claude/skills/
```

## 3. Verify it installed

```bash
ls .claude/skills/
```

You should see `robots-ai-crawler-audit/` (and the others, if you installed the whole pack), each with a `SKILL.md` inside.

## 4. Run it

Open your agent in that project directory and ask, in plain language — no special syntax needed:

> Use the `robots-ai-crawler-audit` skill to check whether AI crawlers (GPTBot, ClaudeBot, PerplexityBot) can reach `<your-site>`. Also check `llms.txt` and `sitemap.xml` aren't soft-blocked — verify the response body, not just the status code.

The agent reads the skill's `SKILL.md` + `references/checks.md` and runs the actual `curl` checks itself — it needs Bash/terminal tool permission, so approve that if prompted. It reports findings with real command output as evidence, per this pack's evidence-discipline convention (no finding without an observed status code or explicit robots.txt rule).

For the full picture instead of just crawler access, ask for the `ai-visibility-audit` skill instead — it's the orchestrator that delegates to all specialist skills (crawler access, sitemap discovery, schema markup, citation readiness, content gaps, `llms.txt`, image visibility, ecommerce catalog technical SEO).

## 5. Don't trust a 200 alone

A `200` status code on `llms.txt` or `sitemap.xml` does not mean the file exists. Two failure modes look identical to a naive status-code check but are easy to catch once you know to look:

- **Soft-block via captcha/anti-bot challenge**: some anti-bot systems (e.g. Alibaba/Taobao's TMD, Cloudflare challenges) return `200` with a JavaScript-redirect captcha page for *any* path, including ones that don't exist. Confirm by hitting a deliberately made-up path (`/this-should-not-exist-xyz`) — if it returns the identical body as `llms.txt`, that "llms.txt" isn't real.
- **SPA-fallback shell**: a single-page app's server can return its `index.html` shell (content-type `text/html`) for any unmatched route, including `/llms.txt`. Check the `content-type` header — a real `llms.txt` should be `text/plain`, and a real `sitemap.xml` should be `application/xml`, not `text/html`.

Always ask your agent to show you the actual response headers and the first few hundred characters of the body, not just the status code.

## 6. What good output looks like

A thorough run reports, per finding: the exact command run, the observed output, and what it means — not an inferred conclusion without evidence. Expect a mix, not a single verdict: a site can have a clean, well-reasoned `robots.txt` and still fail on content visibility (e.g. client-side-rendered pages that a non-JS-executing crawler can't read), or vice versa. Don't expect (or manufacture) a single pass/fail score — the report should separate access (can a crawler reach the page) from content (does the page, as delivered to that crawler, actually say anything).

## 7. Understanding [EXPERIMENTAL] findings

Audits may check emerging draft protocols (Content Signals in `robots.txt`, Web Bot Auth cryptographic verification, DNS-AID SVCB/HTTPS records, Markdown content-negotiation `Accept: text/markdown`, and Auth.md/ARD manifests). When present, these findings are always labeled with **`[EXPERIMENTAL]`** in reports and remediation plans. 

These represent draft specifications and future-readiness signals. Missing an experimental signal does **not** harm search engine discovery, crawler indexing, or AI platform visibility today.

## 8. Exporting client-ready PDF reports

You can ask your AI agent to run an audit and export a formatted executive PDF in a single prompt:

> **Example Prompt:**  
> *"Run an AI visibility audit against `https://example.com/`, format the output using the standardized audit report template, and generate a PDF deliverable in `output/`."*

The agent will execute the audit checks, write `output/example-com-ai-visibility-audit.md`, and run:
```bash
python scripts/render-audit-pdf.py output/example-com-ai-visibility-audit.md
```
This produces `output/example-com-ai-visibility-audit.pdf` with executive typography, severity status pills, and page-break optimization.


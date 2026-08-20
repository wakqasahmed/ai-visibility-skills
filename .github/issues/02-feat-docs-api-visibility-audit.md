# feat(skill): add docs-api-visibility-audit skill

**Labels:** `enhancement`, `skill`, `eval`

## Problem

Developer platforms, APIs, SDKs, and developer-focused SaaS rely heavily on AI coding agents (Claude Code, Cursor, Copilot, Antigravity, ChatGPT) and developer search engines to discover, comprehend, and write code against their APIs. 

Common blockers that render developer documentation invisible or broken for AI agents:
1. **Interactive/SPA-only API docs:** Redoc, Swagger UI, or GraphQL playgrounds rendered entirely client-side without static HTML fallback or raw specification endpoint links.
2. **Missing or undiscoverable OpenAPI / AsyncAPI / JSON Schema specifications:** LLMs produce significantly fewer hallucinated endpoints/parameters when provided structured API specs, but specs are frequently buried or omitted from `llms.txt` and sitemaps.
3. **Un-copyable / un-annotated code blocks:** Code snippets lacking explicit language identifiers (e.g., ` ```typescript ` vs bare ` ``` `), missing SDK version context, or requiring interactive tab clicks to view parameters.
4. **Auth-walled or dynamically generated reference pages:** Documentation URLs returning 401/403 or redirecting AI bots without a crawlable public subset.

Currently, existing skills cover general web content (`answer-engine-content-audit`) and `llms.txt` drafting, but do not specifically test API/developer documentation machine-readability.

## Proposed Scope & Lane

`docs-api-visibility-audit` audits whether developer documentation, API references, SDK guides, and schemas are readily parseable and usable by AI coding assistants and search crawlers.

**In-Scope:**
1. Machine-readable schema availability: checks for raw `openapi.json` / `openapi.yaml` / `schema.json` links in headers, footers, or `<link>` tags.
2. Server-side renderability of API endpoint reference docs (HTTP methods, path parameters, request/response bodies present in initial HTML vs. empty client-side DOM shells).
3. Code sample markup quality: syntax highlighting fencing (`<pre><code class="language-...">`), SDK version notes, and copyability without hidden UI wrappers.
4. Error code & rate limit documentation discoverability.
5. Developer-specific `llms-full.txt` or `/docs/llms.txt` pointer discovery.

**Delegation / Out-of-Scope:**
- General `robots.txt` access belongs to `robots-ai-crawler-audit`.
- Drafting `llms.txt` belongs to `llms-txt-generator`.
- Non-developer consumer content gaps belong to `answer-engine-content-audit`.
- Whole-site visibility triage belongs to `ai-visibility-audit`.

## Citations to Register
- `OPENAPI-SPEC-01`: OpenAPI Initiative, *OpenAPI Specification 3.1.0 / Machine-Readable API Descriptions*.
- `COMMONMARK-CODE-01`: CommonMark / GitHub Flavored Markdown, *Fenced code blocks and info strings for machine-parsing*.

## Acceptance Criteria
- [ ] Create `skills/ai-visibility/docs-api-visibility-audit/SKILL.md` with standard frontmatter, scope, workflow, output format, and guardrails.
- [ ] Create `skills/ai-visibility/docs-api-visibility-audit/references/checks.md` with curl / extraction commands for OpenAPI spec discovery, rendered code-block inspection, and endpoint table parsing.
- [ ] Create `skills/ai-visibility/docs-api-visibility-audit/references/guardrails.md` (and canonical sync).
- [ ] Create `eval/ai-visibility/docs-api-visibility-audit/` containing `contract.py`, `run_eval.py`, `model_harness.py`, `README.md`, and 10 fixtures (5 `should_use`, 5 `should_not_use`).
- [ ] Add `docs-api-visibility-audit` to:
  - `.claude-plugin/plugin.json`
  - `manifest.json` (bump `skill_count` and `source_count`)
  - `README.md` skill table
  - `SOURCES.md` and `SOURCE_INDEX.json`
  - `docs/EXAMPLE_PROMPTS.md`
  - `bench/docs-api-visibility-audit/TODO.md`
  - `skills/ai-visibility/ai-visibility-audit/SKILL.md` (Delegation section)
  - `skills/ai-visibility/ai-search-remediation-plan/references/checks.md`
- [ ] Add deterministic test step to `.github/workflows/ci.yml` and add `.github/workflows/docs-api-visibility-audit-model-eval.yml`.
- [ ] All validators pass: `validate-plugin.py`, `validate-citations.py`, and `run_eval.py`.

## Risk Level
Low — additive new skill with zero breaking changes to existing skills.

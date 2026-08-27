---
name: docs-api-visibility-audit
description: Audit whether developer documentation, REST/GraphQL API references, SDK guides, and OpenAPI schemas are machine-readable, server-rendered, and indexable for AI coding assistants and search bots.
---

# Developer Documentation & API Visibility Audit

Audit technical documentation, API reference portals, OpenAPI/Swagger specifications, and developer guides to ensure AI coding agents (Claude Code, Cursor, Copilot, Antigravity) and search engines can discover, understand, and generate accurate code against your APIs without hallucination.

## Workflow

1. **Discover Machine-Readable API Schemas**:
   - Probe conventional schema paths: `/openapi.json`, `/openapi.yaml`, `/swagger.json`, `/.well-known/openapi.json`, and `<link rel="describedby">` header/HTML tags `[OPENAPI-SPEC-01]`.
   - Verify whether schema files return `200 OK` with valid JSON/YAML syntax and parseable `paths`, `parameters`, `requestBody`, and `responses` definitions.

2. **Audit Server-Side Rendering (SSR) of Reference Pages**:
   - Fetch raw HTML (`curl -s "$URL"`) and verify whether HTTP methods (`GET`, `POST`, `PUT`, `DELETE`), endpoint paths, parameter descriptions, and error codes exist in the initial HTML payload `[OPENAPI-SPEC-01]`.
   - Flag client-side-only SPA doc frameworks (e.g. bare React/Redoc/Swagger UI shells) that deliver an empty `<div id="swagger-ui"></div>` to non-JavaScript AI crawlers.

3. **Verify Code Sample Formatting & Language Tagging**:
   - Inspect code blocks for CommonMark / GFM language info strings (`<pre><code class="language-typescript">`, `<pre><code class="language-python">`) `[COMMONMARK-CODE-01]`.
   - Flag untagged code blocks (`<pre><code>` with no language class) or obfuscated tabbed interfaces that prevent AI models from parsing sample syntax.

4. **Audit Authentication, Error Codes, and Rate Limit Transparency**:
   - Verify that authentication schemes (Bearer tokens, API keys, OAuth endpoints) and HTTP error code tables (400, 401, 403, 429, 500) are documented in structured HTML.

5. **Inspect Developer Agent Pointers (`/docs/llms.txt`)**:
   - Check if the documentation root exposes a curated developer manifest (e.g., `/docs/llms.txt` or `llms-full.txt`) pointing directly to markdown guides and spec downloads.

6. **Classify Findings & Deliver Remediation**:
   - Provide concrete fixes: schema hosting, SSR static generation, language fencing, and developer ticket blueprints.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Core robots.txt access and edge blocking → `robots-ai-crawler-audit`
- Drafting general `/llms.txt` files → `llms-txt-generator`
- Consumer-focused content gap analysis → `answer-engine-content-audit`
- Developer tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Reports must contain:
1. **API Schema Discovery Matrix**: Paths probed, status codes, format, and parseability.
2. **Documentation Renderability & SSR Conformance**: Raw HTML presence of endpoints, methods, and parameters.
3. **Code Sample & Syntax Markup Quality**: Language tagging, fenced code blocks, and copyability.
4. **Recommended Fixes**: Prioritized actions with code/schema blueprints and verification commands.
5. **Verification Commands**: Reproducible curl commands.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for cross-cutting rules on outcome guarantees and factual evidence.

- Distinguish observed HTML/schema endpoints (`High [Measured]`) from inferred API capabilities.
- Do not attempt to test authenticated private endpoints with live credentials (read-only public documentation inspection only).

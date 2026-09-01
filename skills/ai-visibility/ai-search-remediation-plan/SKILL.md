---
name: ai-search-remediation-plan
description: Convert AI visibility, AEO, GEO, crawler, schema, sitemap, and citation audit findings into prioritized implementation tickets or a practical remediation checklist.
---

# AI Search Remediation Plan

Turn audit findings into execution-ready work.

## Workflow

1. Group findings by outcome: discovery, parsing, citation, content, trust, agent protocols, and conversion.
2. Rank each item by impact, effort, risk, and dependency.
3. Convert findings into structured **Master Remediation Blueprints** (see `references/agent_remediation_blueprints.md`) matching the standardized blueprint shape:
   - **Goal**: Clear objective statement citing the underlying protocol / RFC specification (e.g. `[RFC-8288-01]`, `[DNS-AID-01]`, `[MARKDOWN-NEGOTIATION-01]`, `[CONTENT-SIGNALS-01]`, `[RFC-9727-01]`, `[RFC-9728-01]`).
   - **Issue**: Specific observed finding or reproduction command failure.
   - **Fix**: Actionable remediation instructions with exact header, DNS, JSON, HTML, or server configuration snippets.
   - **Skill & Standards**: Direct canonical skill URLs and IETF/W3C/RFC documentation links.
4. Include acceptance criteria and verification commands (`curl`, `dig`, or schema validators) for each item.
5. Mark work that needs owner approval, policy decisions, credentials, CMS access, or legal review.

## Output

- **Priority Roadmap**: Ranked list of remediation milestones.
- **Master Remediation Blueprints**: Structured cards containing Goal, Issue, Fix, Recipe, Skill reference, and RFC Docs.
- **Acceptance Criteria & Verification Commands**: Re-runnable CLI validation commands.
- **Owner Decisions & HITL Blockers**: Explicit list of human-only approvals.

## Guardrails

- Keep tasks independently executable where practical.
- Do not bundle broad content strategy, technical SEO, and schema changes into one vague ticket.
- Make human-only blockers explicit before implementation starts.

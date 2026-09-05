---
name: ai-search-remediation-plan
description: Convert AI visibility, AEO, GEO, crawler, schema, sitemap, and citation audit findings into prioritized implementation tickets or a practical remediation checklist.
---

# AI Search Remediation Plan

Turn audit findings into execution-ready work.

## Workflow

1. Group findings by outcome: discovery, parsing, citation, content, trust, and conversion.
2. Classify each finding by evidence tier, then rank it by impact, effort, risk, and dependency:
   - *Tier 1 — Critical Foundation*: Directly blocks crawling, indexing, or core entity understanding.
   - *Tier 2 — Important Improvement*: Meaningfully impacts discoverability, answer extraction, or trust.
   - *Tier 3 — Supporting Signal*: General hygiene and secondary signals.
   - *Tier 4 — Experimental Protocol*: Emerging draft conventions (`llms.txt`, ARD, DNS-AID, Content Signals) — *never reduces the core 100-point audit score*.
   - Assign every finding to P0 (Immediate), P1 (Next), P2 (Improve), or P3 (Optional/Experimental).
3. Convert the top items into tickets or checklist steps.
4. Include acceptance criteria and verification for each item, using [references/checks.md](references/checks.md) to carry forward the source audit's re-runnable check.
5. Mark work that needs owner approval, policy decisions, credentials, CMS access, or legal review.

## Output

- **Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), P3 (Optional/Experimental) backlog.
- **Evidence Tier**: Label every item Tier 1 — Critical Foundation, Tier 2 — Important Improvement, Tier 3 — Supporting Signal, or Tier 4 — Experimental Protocol.
- **Technical Appendix**: Developer tickets with delegate skills, blueprints, and verification commands.
- **Ticket Detail**: Acceptance criteria, owner decisions, and blockers for every developer ticket.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for the cross-cutting rules on outcome guarantees, factual evidence, and private paths.

- Keep tasks independently executable where practical.
- Do not bundle broad content strategy, technical SEO, and schema changes into one vague ticket.
- Make human-only blockers explicit before implementation starts.

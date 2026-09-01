---
name: semantic-entity-topical-map-audit
description: Audit entity disambiguation, knowledge graph grounding (sameAs links to Wikidata/Crunchbase), and topical cluster completeness for generative AI search engines.
---

# Semantic Entity & Topical Map Audit

Audit whether a website establishes clear entity identity in the global knowledge graph and demonstrates topical authority through structured semantic relationships, enabling AI answer engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) to disambiguate, understand, and cite the brand accurately `[SCHEMA-ORGANIZATION-01]`.

## Workflow

1. **Audit Entity Disambiguation & `sameAs` Knowledge Graph Grounding**:
   - Inspect Schema.org `Organization`, `Brand`, and `Person` JSON-LD entities on the homepage and about/author pages `[SCHEMA-ORGANIZATION-01]`.
   - Verify presence of canonical `sameAs` array pointing to authoritative external knowledge bases:
     - Wikidata URI (e.g. `https://www.wikidata.org/wiki/Q...`).
     - Wikipedia article URI.
     - Crunchbase organization URI.
     - Official verified social profiles (LinkedIn, X/Twitter, GitHub, YouTube).
   - Ensure the entity `@id` uses a stable global URI (e.g. `https://example.com/#organization`).

2. **Audit Entity Graph Reconciliation Across Nested Schemas**:
   - Check that `Article` (publisher/author), `WebSite` (publisher), and `Product` (brand/manufacturer) reference the canonical `@id` rather than duplicating disconnected anonymous entity objects `[SCHEMA-ORGANIZATION-01]`.
   - Ensure author entities include `JobTitle`, `alumniOf`, `worksFor`, and author `sameAs` profiles for E-E-A-T grounding.

3. **Audit Topical Map Completeness & Pillar-Cluster Architecture**:
   - Analyze internal linking structure between core pillar pages and supporting subtopic cluster articles.
   - Verify that subtopic pages link back to the pillar with descriptive, semantic anchor text.
   - Flag content orphan clusters that lack hierarchical semantic parent references.

4. **Classify Entity Ambiguity Risk & Deliver Remediation**:
   - Classify entity clarity as `AMBIGUOUS`, `PARTIALLY_GROUNDED`, or `FULLY_RECONCILED`.
   - Deliver ready-to-deploy JSON-LD entity graph templates with Wikidata reconciliation.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Core JSON-LD schema syntax and validator checks → `schema-markup-audit`
- Answer engine content gap analysis → `answer-engine-content-audit`
- Developer implementation tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Report entity identification score, missing `sameAs` knowledge graph links, topical cluster graph depth, and copy-pasteable JSON-LD graph snippets.

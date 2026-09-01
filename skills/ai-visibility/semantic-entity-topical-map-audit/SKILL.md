---
name: semantic-entity-topical-map-audit
description: Audit entity disambiguation, knowledge graph grounding (sameAs reference pages such as Wikidata), and topical pillar-cluster completeness for generative AI search engines.
---

# Semantic Entity & Topical Map Audit

Audit whether a website states its entity identity unambiguously in machine-readable form and organizes its content into a coherent pillar-and-cluster topical structure, so that search engines and AI answer engines have a reconcilable identity to attach claims to instead of guessing between same-named entities.

Schema.org defines `sameAs` as the "URL of a reference Web page that unambiguously indicates the item's identity", naming an item's Wikipedia page, Wikidata entry, or official website as the examples `[SCHEMA-SAMEAS-01]`. Google's `Organization` structured-data guidance frames `sameAs` more broadly as "the URL of a page on another website with additional information about your organization" — for example a profile page on a social media or review site — and does not name Wikidata or Crunchbase specifically `[GOOGLE-ORG-SCHEMA-01]`. Treat Wikidata and Wikipedia as the identity-reconciliation targets Schema.org actually names, and treat Crunchbase, LinkedIn, GitHub and similar profiles as additional corroborating references.

No first-party documentation from OpenAI, Perplexity, Google, or Anthropic establishes `sameAs` as an input to their entity resolution. Do not assert that adding `sameAs` causes a named engine to disambiguate, cite, or recommend a brand. State the mechanism as what it verifiably is: an unambiguous machine-readable identity claim that removes a source of confusion.

## Workflow

1. **Audit entity disambiguation and `sameAs` knowledge graph grounding**:
   - Inspect Schema.org `Organization`, `Brand`, and `Person` JSON-LD entities on the homepage and about/author pages `[SCHEMA-ORGANIZATION-01]`.
   - Check for a `sameAs` array pointing at reference pages that unambiguously indicate identity `[SCHEMA-SAMEAS-01]`:
     - Wikidata item URI (`https://www.wikidata.org/wiki/Q...`) and/or Wikipedia article URI — the examples Schema.org names.
     - Corroborating profiles: Crunchbase organization page and official verified social profiles (LinkedIn, X/Twitter, GitHub, YouTube) `[GOOGLE-ORG-SCHEMA-01]`.
   - Ensure the entity `@id` uses a stable global URI (e.g. `https://example.com/#organization`).
   - Where a `sameAs` target is present, resolve it and confirm it describes this organization before reporting it as reconciled — a presence grep proves the property is *present*, not that the target is correct `[WIKIDATA-DATA-ACCESS-01]`.

2. **Audit entity graph reconciliation across nested schemas**:
   - Check that `Article` (publisher/author), `WebSite` (publisher), and `Product` (brand/manufacturer) reference the canonical `@id` rather than duplicating disconnected anonymous entity objects `[SCHEMA-ORGANIZATION-01]` `[SCHEMA-ARTICLE-01]`.
   - Check author entities for `jobTitle`, `alumniOf`, `worksFor`, and author `sameAs` profiles `[SCHEMA-PERSON-01]`. Note the exact casing: the Schema.org property is `jobTitle`, not `JobTitle`.
   - Google's guidance is about reader-visible authorship: it "strongly encourage[s] adding accurate authorship information, such as bylines to content where readers might expect it" `[GOOGLE-EEAT-AUTHOR-01]`. Structured `Person` markup is the machine-readable expression of that same byline information; it is industry practice rather than a documented E-E-A-T ranking input, so report gaps as markup-completeness gaps, not as scoring signals.

3. **Audit topical map completeness and pillar-cluster architecture**:
   - A topic cluster is a page focused on a topic, a cluster of pages covering related subtopics in more depth, and internal linking between all of them — the same structure also called a content hub or pillar-and-spoke `[AHREFS-TOPIC-CLUSTERS-01]`.
   - Analyze internal linking between core pillar pages and supporting subtopic pages, in both directions.
   - Verify that subtopic pages link back to the pillar with descriptive, semantic anchor text.
   - Flag orphan subtopic pages that have no internal link path from their pillar `[BACKLINKO-ORPHAN-PAGES-01]`.

4. **Classify entity clarity and deliver remediation**:
   - Emit exactly one classification, on a line reading `Entity clarity classification: **VALUE**`, where `VALUE` is one of:
     - `AMBIGUOUS` — no `sameAs` reference pages and/or no stable entity `@id`; nothing machine-readable pins the identity down.
     - `PARTIALLY_GROUNDED` — some reference pages or `@id` linkage present, but the entity graph or the author entities are incomplete.
     - `FULLY_RECONCILED` — stable `@id`, resolved `sameAs` reference pages, and consistent `@id` reuse across nested entities.
   - Use these three literals only. Do not invent additional labels, and do not report a numeric entity score — this skill defines no scoring scale, so a number here would be fabricated.
   - Deliver ready-to-deploy JSON-LD entity graph templates. Every Wikidata Q-id in a template must be an unresolved placeholder (`Q00000000`), with an instruction to resolve the organization's real Q-id first — a copy-pasted real Q-id asserts identity with an unrelated entity, which is worse than having no `sameAs` at all.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Core JSON-LD schema syntax and validator checks → `schema-markup-audit`
- Answer engine content gap analysis → `answer-engine-content-audit`
- Developer implementation tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Reports must contain these sections, in this order:

1. **Entity Disambiguation & Knowledge Graph Grounding**: target, the `Entity clarity classification: **VALUE**` line, detected `@id`, and detected `sameAs` reference pages.
2. **Schema Graph Reconciliation**: whether nested `Article`/`WebSite`/`Product` entities reuse the canonical `@id`, and the state of author `Person` entities.
3. **Topical Map & Cluster Structure**: pillar pages, cluster depth, and any orphan subtopic pages.
4. **Recommended Fixes & Schema Graph**: prioritized fixes with copy-pasteable JSON-LD using placeholder Q-ids.
5. **Verification Commands**: the reproducible commands from [`references/checks.md`](references/checks.md) that produced each finding.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for cross-cutting rules on outcome guarantees and factual evidence.

- **No outcome guarantees**: do not claim or imply that adding `sameAs`, an `@id`, or cluster links guarantees inclusion, ranking, or citation in any AI engine. Describe a recommendation as removing an identified ambiguity, not as producing an outcome.
- **No fabricated third-party behaviour**: never state that a named engine (ChatGPT, Perplexity, Gemini, Claude) confuses, conflates, or resolves a specific entity unless the report quotes an observed, pasted answer as evidence. Findings backed by command output are `High [Measured]`; anything weaker is `Medium [Derived]` and must be written as an inference about the markup, not as an observation of an engine.
- **No invented counts or statistics**: entity, competitor, and cluster counts must come from command output or user-supplied data, never from estimation. State the URL set a count was computed over, and never extrapolate beyond it.
- **"Present" is not "verified"**: report a `sameAs` target as `present` when only a presence check ran, and as `verified` only when the target was resolved (check 2 in [`references/checks.md`](references/checks.md)) and confirmed to describe this organization.
- **A check that could not run is not a passing check**: if there is no pillar page to compare against, report orphan detection as not-run rather than as zero orphans.

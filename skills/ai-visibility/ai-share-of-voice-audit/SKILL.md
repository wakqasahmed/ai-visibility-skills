---
name: ai-share-of-voice-audit
description: Audit brand mention frequency, citation share of voice (SoV), and competitor displacement across ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews.
---

# AI Share of Voice (SoV) & Multi-Model Citation Audit

Evaluate brand presence, mention frequency, citation share of voice, and competitive positioning across generative answer engines (ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews) `[PERPLEXITY-BOTS-01]` on core ICP queries, inspired by enterprise observation frameworks from DataForSEO, Keytomic, and Profound.

## Workflow

1. **Define ICP Query Corpus & Competitor Cohort**:
   - Assemble representative queries across 3 intent tiers:
     - Commercial / comparative: *"best [category] software"*, *"[brand] vs [competitor]"*.
     - Problem-solving / educational: *"how to fix [problem]"*.
     - Transactional / feature-specific: *"[feature] pricing and alternatives"*.
   - Identify 3–5 direct market competitors in the category.

2. **Audit Multi-Model Brand Mentions & Source Citations**:
   - Inspect answer transcripts across AI engines (ChatGPT with search `[OPENAI-BOTS-01]`, Claude Search `[ANTHROPIC-BOTS-01]`, Perplexity `[PERPLEXITY-BOTS-01]`, Gemini / Google AI Overviews `[GOOGLE-EXTENDED-01]`).
   - Extract:
     - **Mention status**: `MENTIONED`, `UNMENTIONED`, or `EXCLUDED`.
     - **Citation status**: Cited URL link present vs unlinked text mention.
     - **Positioning**: Ranked order of recommendation (#1 choice, alternative, or disclaimer).
     - **Sentiment**: `POSITIVE`, `NEUTRAL`, or `NEGATIVE`.

3. **Calculate Share of Voice (SoV) & Competitor Displacement**:
   - Compute Brand SoV percentage: $\text{SoV} = \frac{\text{Brand Mentions}}{\text{Total Category Mentions}} \times 100\%$.
   - Identify **displacement gaps**: High-volume queries where competitors are consistently recommended but the target brand is absent.
   - Trace displaced queries back to source URLs cited for competitors to identify missing content assets.

4. **Classify Visibility Posture & Deliver Remediation**:
   - Classify posture as `DOMINANT` ($\ge 60\%$), `COMPETITIVE` ($30\text{--}59\%$), `EMERGING` ($10\text{--}29\%$), or `INVISIBLE` ($<10\%$).
   - Deliver actionable content and schema playbooks to displace competitors on target queries.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Citation readiness and anchor stability → `citation-readiness-audit`
- Content gap analysis for unmentioned queries → `answer-engine-content-audit`
- Developer implementation tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Report query-by-query multi-model matrix, computed Share of Voice percentage, competitor displacement breakdown, and prioritized content remediation tasks.

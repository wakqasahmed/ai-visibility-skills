---
name: ai-share-of-voice-audit
description: Audit brand mention frequency, citation share of voice (SoV), and competitor displacement across ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews.
---

# AI Share of Voice (SoV) & Multi-Model Citation Audit

Evaluate brand presence, mention frequency, citation share of voice, and competitive positioning across generative answer engines (ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews) on core ICP queries.

Answer transcripts are supplied by the operator (pasted or exported). This skill does not query answer engines or third-party observation APIs on its own, and every figure it reports is a sample statistic over the corpus the operator supplied — not a platform-reported metric.

Transcript capture format, classification procedure, and the SoV computation live in [references/checks.md](references/checks.md).

## Workflow

1. **Define ICP Query Corpus & Competitor Cohort**:
   - Assemble representative queries across 3 intent tiers:
     - Commercial / comparative: *"best [category] software"*, *"[brand] vs [competitor]"*.
     - Problem-solving / educational: *"how to fix [problem]"*.
     - Transactional / feature-specific: *"[feature] pricing and alternatives"*.
   - Identify 3–5 direct market competitors in the category. This cohort fixes the SoV denominator, so record it explicitly (see step 3).
   - Record corpus size, engine list, and capture date before computing any figure — see [references/checks.md](references/checks.md) section 1 for the capture record format.

2. **Audit Multi-Model Brand Mentions & Source Citations**:
   - Inspect operator-supplied answer transcripts from AI engines (ChatGPT with search `[OPENAI-BOTS-01]`, Claude Search `[ANTHROPIC-BOTS-01]`, Perplexity `[PERPLEXITY-BOTS-01]`, Gemini / Google AI Overviews `[GOOGLE-EXTENDED-01]`).
   - Extract, per transcript:
     - **Mention status**: `MENTIONED`, `UNMENTIONED`, or `EXCLUDED`.
     - **Citation status**: Cited URL link present vs unlinked text mention.
     - **Positioning**: Ranked order of recommendation (#1 choice, alternative, or disclaimer).
     - **Sentiment**: `POSITIVE`, `NEUTRAL`, or `NEGATIVE`, applied to quoted transcript text.

3. **Calculate Share of Voice (SoV) & Competitor Displacement**:
   - Define the denominator once, and use only this definition:
     - `Total Category Mentions` = brand mentions + mentions of the tracked competitor cohort from step 1, counted across the sampled transcripts. It is **not** "all mentions in the category" — it is cohort-scoped, so adding or dropping a tracked competitor changes every percentage. State the cohort next to the figure.
   - `SoV % = brand mentions / Total Category Mentions * 100`
   - Every reported percentage must be recomputable from mention counts printed in the same report, in the form `brand / total = pct%`. If a figure cannot be recomputed from printed counts, do not report it.
   - Identify **displacement gaps**: queries where cohort competitors are consistently recommended but the target brand is absent.
   - Trace displaced queries back to source URLs cited for competitors to identify missing content assets.

4. **Classify Visibility Posture & Deliver Remediation**:
   - Posture bands are an internal convention of this skill, not an industry standard, and no source establishes them: `DOMINANT (>= 60%)`, `COMPETITIVE (30-59%)`, `EMERGING (10-29%)`, `INVISIBLE (< 10%)`.
   - Minimum corpus for a posture label: at least 20 prompts across at least 2 engines. Below that floor, report raw counts and label the posture `INDICATIVE ONLY (corpus below floor)` instead of assigning a band.
   - Deliver actionable content and schema playbooks to displace competitors on target queries.

## Delegation

- Whole-site visibility scoring and orchestration → `ai-visibility-audit`
- Citation readiness and anchor stability → `citation-readiness-audit`
- Content gap analysis for unmentioned queries → `answer-engine-content-audit`
- Developer implementation tickets and roadmaps → `ai-search-remediation-plan`

## Output Format

Report query-by-query multi-model matrix, computed Share of Voice percentage, competitor displacement breakdown, and prioritized content remediation tasks.

Reports must contain:
1. **Multi-Model Brand Mention & Citation Matrix**: engines, prompt-corpus size, capture date, per-query mention and citation status.
2. **Share of Voice Calculation & Benchmark**: the tracked cohort, `Total Category Mentions`, and every SoV percentage printed as `brand / total = pct%`.
3. **Competitor Displacement & Source Attribution**: displaced queries with the competitor source cited in the transcript.
4. **Prioritized Remediation & Displacement Playbook**.
5. **Verification Methodology**: capture record and reproducible commands.

## Guardrails

See [Shared Guardrails](references/guardrails.md) for cross-cutting rules on outcome guarantees and factual evidence, and [references/checks.md](references/checks.md) for the capture and computation procedures.

- Distinguish observed answer transcripts (`High [Measured]`) from extrapolated category share of voice (`Medium [Derived]`). Label every figure with one of the two.
- Every SoV figure must state its prompt-corpus size, engine list, and capture date. Answer engines are non-deterministic: a re-run on the same corpus will not reproduce the same numbers, so an undated figure is not interpretable.
- Answer transcripts must be operator-supplied or pasted, never asserted from memory. Do not autonomously query answer engines or paid third-party observation APIs.
- Do not name real third-party companies as observed competitors, citation sources, or sentiment drivers unless that name appears in a transcript the operator supplied. Illustrative examples must use clearly fictional names.
- Sentiment counts require the per-transcript labels they come from: report `12 / 15 POSITIVE [Measured]`, never a bare `95% Positive`.

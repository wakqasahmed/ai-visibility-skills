# AI Share of Voice Audit: AcmeAI

## Multi-Model Brand Mention & Citation Matrix

Capture date: 2026-09-04. Corpus: 3 prompts across ChatGPT, Claude, and Perplexity. Tracked cohort: AcmeAI and RivalOne.

| Engine | AcmeAI | RivalOne | Citation evidence |
|---|---|---|---|
| ChatGPT | UNMENTIONED | MENTIONED | `https://rivalone.example/product` |
| Claude | MENTIONED | MENTIONED | `https://acmeai.example/product` |
| Perplexity | UNMENTIONED | MENTIONED | `https://rivalone.example/product` |

## Share of Voice Calculation & Benchmark

AcmeAI has `1 / 4 = 25.0%` share of voice in the AcmeAI/RivalOne cohort `[Measured]`. The corpus is below the 20-prompt and two-engine posture floor, so the posture is `INDICATIVE ONLY (corpus below floor)`.

## Competitor Displacement & Source Attribution

RivalOne displaces AcmeAI in the ChatGPT and Perplexity transcripts, both of which cite `https://rivalone.example/product`. This is `Medium [Derived]` from the supplied transcript evidence.

## Prioritized Remediation & Displacement Playbook

1. Compare the cited RivalOne product page with AcmeAI's product page for claims that directly answer the sampled query.
2. Use the content-gap findings to brief `answer-engine-content-audit`; do not infer performance beyond this corpus.

## Verification Methodology

The audit classified only the three pasted transcripts. Recompute the cohort figure with `python3 -c "print(round(1 / 4 * 100, 1))"`; it returns `25.0`.

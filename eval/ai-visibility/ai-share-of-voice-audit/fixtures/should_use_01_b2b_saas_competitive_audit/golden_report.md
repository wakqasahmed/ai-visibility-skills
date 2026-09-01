# AI Share of Voice Report: crmpro.example

All entities in this report are fictional illustrative names.

## Multi-Model Brand Mention & Citation Matrix

- Target: `crmpro.example` (CRMPro)
- Engines: ChatGPT Search, Claude Search, Perplexity, Google AI Overviews (4 engines)
- Prompt corpus: 20 prompts (8 commercial/comparative, 6 problem-solving, 6 transactional)
- Capture date: 2026-08-24 (logged-out, US / en-US, web UI)
- Tracked cohort: CRMPro + SalesHub + PipelineX
- Unstable prompts on re-capture: 2 of 20

| Intent tier | Prompts | `MENTIONED` | `CITED` | `EXCLUDED` |
|---|:---:|:---:|:---:|:---:|
| Commercial / comparative | 8 | 5 | 4 | 0 |
| Problem-solving | 6 | 4 | 2 | 0 |
| Transactional / feature | 6 | 3 | 2 | 0 |
| **Total** | **20** | **12** | **8** | **0** |

Brand mention rate: 12 of 20 prompts `MENTIONED` [Measured]. Cited URL present in 8 of 20 [Measured].

## Share of Voice Calculation & Benchmark

Cohort mention counts over the same 20 prompts:

```text
Total Category Mentions (cohort: CRMPro + SalesHub + PipelineX) = 12 + 15 + 7 = 34
CRMPro:    12 / 34 = 35.3% [Measured]
SalesHub:  15 / 34 = 44.1% [Measured]
PipelineX:  7 / 34 = 20.6% [Measured]
```

Cohort shares sum to 100.0% by construction. Posture: `COMPETITIVE` (30-59% band, an internal convention of this skill). Corpus of 20 prompts across 4 engines meets the floor for assigning a band.

## Competitor Displacement & Source Attribution

- `"best mid-market crm"` — CRMPro `UNMENTIONED`; SalesHub cited from a third-party software-comparison directory listing in the Perplexity source list [Measured].
- `"open-source crm alternatives"` — CRMPro `UNMENTIONED` on 3 of 3 engines that answered [Measured].
- Displacement pattern [Derived]: on comparative intent the cohort competitors hold a directory-listing citation and CRMPro does not, which is the most likely driver of the 8.8-point gap to SalesHub.

## Prioritized Remediation & Displacement Playbook

1. Publish a mid-market comparison matrix page with `Product` and `Review` structured data, targeting the two `UNMENTIONED` comparative prompts.
2. Publish verified integration documentation to create citable anchors for the transactional-intent prompts.
3. Re-capture the same 20 prompts in 30 days to establish a second dated batch; a single batch is not a trend.

## Verification Methodology

Capture record per engine (engine, surface, account state, locale, capture date, prompt count) is stored with the pasted transcripts. Target-side reachability of the cited anchors was re-checked:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L "https://crmpro.example/pricing"
```

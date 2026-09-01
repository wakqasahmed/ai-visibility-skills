# AI Share of Voice Report: ecohome.example

All entities and publications in this report are fictional illustrative names.

## Multi-Model Brand Mention & Citation Matrix

- Target: `ecohome.example` (EcoHome, sustainable furniture)
- Engines: Perplexity, Google AI Overviews (2 engines)
- Prompt corpus: 25 prompts (shopping and comparison intent)
- Capture date: 2026-08-28 (logged-out, US / en-US, web UI)
- Tracked cohort: EcoHome + HomeNest + GreenLoft + TimberEdge
- Unstable prompts on re-capture: 4 of 25

| Status | Prompts |
|---|:---:|
| `MENTIONED` | 7 |
| `UNMENTIONED` | 15 |
| `EXCLUDED` | 3 |
| `CITED` | 2 |

EcoHome is `MENTIONED` in 7 of 25 prompts and `CITED` in only 2 [Measured]. Three prompts are `EXCLUDED` (no AI Overview panel shown) and leave both share-of-voice terms. The gap between 7 mentions and 2 cited URLs is the notable finding: the brand is named more often than it is linked.

## Share of Voice Calculation & Benchmark

```text
Total Category Mentions (cohort: EcoHome + HomeNest + GreenLoft + TimberEdge) = 7 + 11 + 9 + 5 = 32
EcoHome:    7 / 32 = 21.9% [Measured]
HomeNest:  11 / 32 = 34.4% [Measured]
GreenLoft:  9 / 32 = 28.1% [Measured]
TimberEdge: 5 / 32 = 15.6% [Measured]
```

Posture: `EMERGING` (10-29% band, an internal convention of this skill). Corpus of 25 prompts across 2 engines meets the floor, though 4 `UNSTABLE` prompts mean the figure should be read as approximate.

## Competitor Displacement & Source Attribution

- `"best sustainable dining chairs"` — EcoHome `UNMENTIONED`; the answer was assembled from a third-party review roundup on *The Dwell Review* (fictional publication) that lists the cohort competitors and not EcoHome [Measured].
- `"eco furniture vs conventional cost"` — EcoHome `MENTIONED` but `UNLINKED`, with no URL in the source list [Measured].
- Displacement pattern [Derived]: on shopping intent the engines prefer aggregated review roundups over individual storefronts, so a brand absent from those roundups is unlikely to be cited even when it is named.

## Prioritized Remediation & Displacement Playbook

1. Publish comparison guides with `ItemList` and `Product` structured data so a storefront page can serve as the citable source on comparison intent.
2. Add specific, extractable product attributes (materials, certifications, dimensions, price) to category pages, addressing the mention-without-citation gap.
3. Pursue inclusion in category review roundups; the citation evidence shows those pages, not storefronts, are what the engines cited on 15 of 25 prompts.
4. Re-capture the same 25 prompts in 30 days, and track the `EXCLUDED` count separately since AI Overview panels do not appear consistently.

## Verification Methodology

Capture record per engine (engine, surface, account state, locale, capture date, prompt count) is stored with the pasted transcripts. Category page crawlability checked:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L "https://ecohome.example/collections/chairs"
```

# AI Share of Voice Report: newfintech.example

All entities in this report are fictional illustrative names.

## Multi-Model Brand Mention & Citation Matrix

- Target: `newfintech.example` (NewFintech)
- Engines: ChatGPT Search, Claude Search, Perplexity (3 engines)
- Prompt corpus: 20 prompts (developer payment-gateway intent)
- Capture date: 2026-08-25 (logged-out, US / en-US, web UI)
- Tracked cohort: NewFintech + PayRail + Ledgerly + Transactly
- Unstable prompts on re-capture: 0 of 20

| Status | Prompts |
|---|:---:|
| `MENTIONED` | 0 |
| `UNMENTIONED` | 20 |
| `EXCLUDED` | 0 |
| `CITED` | 0 |

NewFintech is `UNMENTIONED` in 20 of 20 transcripts [Measured]. No transcript contained a URL on the brand's domain [Measured].

## Share of Voice Calculation & Benchmark

```text
Total Category Mentions (cohort: NewFintech + PayRail + Ledgerly + Transactly) = 0 + 14 + 9 + 5 = 28
NewFintech:  0 / 28 =  0.0% [Measured]
PayRail:    14 / 28 = 50.0% [Measured]
Ledgerly:    9 / 28 = 32.1% [Measured]
Transactly:  5 / 28 = 17.9% [Measured]
```

Posture: `INVISIBLE` (< 10% band, an internal convention of this skill). The cohort competitors take every mention in this corpus; note that this is a statement about these 20 prompts on these 3 engines on this date, not about the category as a whole.

## Competitor Displacement & Source Attribution

- Cohort competitors were cited from developer-documentation and third-party comparison pages in the Perplexity source lists [Measured].
- No transcript cited NewFintech from any source, including its own documentation [Measured].
- Likely cause [Derived]: the brand has no third-party citation surface and no structured entity record, so there is no source for an engine to cite even when the query matches its category.

## Prioritized Remediation & Displacement Playbook

1. Establish a structured entity record and claim the brand's public company profiles, so an entity lookup resolves.
2. Publish a developer-first payment-gateway comparison page with concrete, citable specifics (limits, currencies, latency figures) rather than positioning copy.
3. Re-capture the same 20 prompts in 30 days; movement off 0.0% on any engine is the first signal to look for.

## Verification Methodology

Capture record per engine (engine, surface, account state, locale, capture date, prompt count) is stored with the pasted transcripts. Brand-side crawlability of the pages that would be cited:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L "https://newfintech.example/docs"
```

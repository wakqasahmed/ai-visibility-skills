# AI Share of Voice Report: hostingfast.example

All entities in this report are fictional illustrative names.

## Multi-Model Brand Mention & Citation Matrix

- Target: `hostingfast.example` (HostingFast)
- Engines: Claude Search, Gemini (2 engines)
- Prompt corpus: 22 prompts (reliability and uptime intent)
- Capture date: 2026-08-27 (logged-out, US / en-US, web UI)
- Tracked cohort: HostingFast + StackHost + NimbusServe + GridFrame
- Unstable prompts on re-capture: 1 of 22

| Status | Prompts |
|---|:---:|
| `MENTIONED` | 8 |
| `UNMENTIONED` | 12 |
| `EXCLUDED` | 2 |
| `CITED` | 4 |

HostingFast is `MENTIONED` in 8 of 22 prompts and `CITED` in 4 [Measured]. Two prompts are `EXCLUDED` (no AI panel returned) and leave both share-of-voice terms.

Sentiment over the 8 mentions, each label taken from a quoted clause: 0 `POSITIVE`, 3 `NEUTRAL`, 5 `NEGATIVE` [Measured]. Example quoted clause: "HostingFast is cheap but has had reliability complaints" (`NEGATIVE`). The negative clauses in 4 of those 5 transcripts were cited from a community forum thread, not from the brand's own status page [Measured].

## Share of Voice Calculation & Benchmark

```text
Total Category Mentions (cohort: HostingFast + StackHost + NimbusServe + GridFrame) = 8 + 17 + 12 + 6 = 43
HostingFast:  8 / 43 = 18.6% [Measured]
StackHost:   17 / 43 = 39.5% [Measured]
NimbusServe: 12 / 43 = 27.9% [Measured]
GridFrame:    6 / 43 = 14.0% [Measured]
```

Posture: `EMERGING` (10-29% band, an internal convention of this skill), and at risk — 5 of the 8 mentions carry `NEGATIVE` sentiment, so raw presence overstates the brand's standing here. Corpus of 22 prompts across 2 engines meets the floor.

## Competitor Displacement & Source Attribution

- `"most reliable cloud hosting"` — HostingFast `UNMENTIONED`; StackHost and NimbusServe cited from their own published uptime pages [Measured].
- `"hostingfast reliability"` — `MENTIONED` with `NEGATIVE` sentiment on both engines, cited from a community forum thread [Measured].
- Displacement pattern [Derived]: the cohort competitors publish first-party uptime evidence and the brand does not, so on reliability intent the only citable source about the brand is third-party complaint discussion.

## Prioritized Remediation & Displacement Playbook

1. Publish a public status and historical-uptime page with machine-readable figures, giving engines a first-party source to cite on reliability intent.
2. Publish a dated, specific post-mortem for the incident being referenced; a transparent account is citable, whereas silence leaves the forum thread as the only source.
3. Add `Service` and `FAQPage` structured data to the reliability page.
4. Re-capture the same 22 prompts in 30 days and track the `NEGATIVE` count, not just the percentage — sentiment can improve while share of voice stays flat.

## Verification Methodology

Capture record per engine (engine, surface, account state, locale, capture date, prompt count) is stored with the pasted transcripts. First-party status surface checked:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L "https://hostingfast.example/status"
```

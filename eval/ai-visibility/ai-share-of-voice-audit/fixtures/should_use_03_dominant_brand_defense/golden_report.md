# AI Share of Voice Report: cloudauth.example

All entities in this report are fictional illustrative names.

## Multi-Model Brand Mention & Citation Matrix

- Target: `cloudauth.example` (CloudAuth)
- Engines: ChatGPT Search, Perplexity (2 engines)
- Prompt corpus: 28 prompts (12 commercial/comparative, 8 problem-solving, 8 transactional)
- Capture date: 2026-08-26 (logged-out, US / en-US, web UI)
- Tracked cohort: CloudAuth + AuthBridge + KeyGate
- Unstable prompts on re-capture: 3 of 28

| Status | Prompts |
|---|:---:|
| `MENTIONED` | 19 |
| `UNMENTIONED` | 8 |
| `EXCLUDED` | 1 |
| `CITED` | 15 |

CloudAuth is `MENTIONED` in 19 of 28 prompts and `CITED` in 15 [Measured]. One prompt is `EXCLUDED` (engine refused to answer) and leaves both share-of-voice terms.

Sentiment over the 19 mentions, each label taken from a quoted clause in the transcript: 16 `POSITIVE`, 3 `NEUTRAL`, 0 `NEGATIVE` [Measured]. Example quoted clause: "CloudAuth is the usual default for teams that need SAML on day one" (`POSITIVE`).

## Share of Voice Calculation & Benchmark

```text
Total Category Mentions (cohort: CloudAuth + AuthBridge + KeyGate) = 19 + 6 + 3 = 28
CloudAuth:  19 / 28 = 67.9% [Measured]
AuthBridge:  6 / 28 = 21.4% [Measured]
KeyGate:     3 / 28 = 10.7% [Measured]
```

Posture: `DOMINANT` (>= 60% band, an internal convention of this skill). Corpus of 28 prompts across 2 engines meets the floor. Note that 3 of 28 prompts were `UNSTABLE` across re-captures, so treat the figure as approximate to within a few points rather than exact.

## Competitor Displacement & Source Attribution

- `"free tier authentication library"` — CloudAuth `UNMENTIONED`; open-source libraries recommended instead, cited from package-registry pages [Measured].
- `"self-hosted sso"` — CloudAuth `UNMENTIONED` on both engines; AuthBridge cited from its own self-hosting guide [Measured].
- Exposure [Derived]: the eight `UNMENTIONED` prompts cluster on free-tier and self-hosted intent, which the brand's documentation does not address, so a competitor answer is the only citable option there.

## Prioritized Remediation & Displacement Playbook

1. Publish a free-tier limits and pricing page with concrete quota figures, addressing the free-tier prompt cluster.
2. Publish a self-hosting and data-residency guide to create a citable source for the self-hosted cluster.
3. Re-capture the same 28 prompts monthly and track the `UNSTABLE` count alongside the percentage; a dominant share can erode without any single prompt flipping permanently.

## Verification Methodology

Capture record per engine (engine, surface, account state, locale, capture date, prompt count) is stored with the pasted transcripts. Cited documentation anchors were re-checked:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L "https://cloudauth.example/docs"
```

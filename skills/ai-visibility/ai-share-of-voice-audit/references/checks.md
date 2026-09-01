# AI Share of Voice Verification Checks

Use these read-only inspections to evaluate brand share of voice. All transcript text is
supplied by the operator; nothing here queries an answer engine automatically.

---

## 1. Multi-Model Transcript Capture & Classification

### 1.1 Corpus size

Per engine, ask the operator to capture at least:

| Intent tier | Minimum prompts |
|---|---|
| Commercial / comparative (`best X`, `X vs Y`) | 8 |
| Problem-solving / educational (`how to ...`) | 6 |
| Transactional / feature-specific (`X pricing`, `X alternatives`) | 6 |

Floor for assigning a posture band: **20 prompts across at least 2 engines**. Below that,
report raw counts and mark the posture `INDICATIVE ONLY (corpus below floor)`.

### 1.2 Capture record (required, one per engine)

Ask the operator to record this block with each transcript batch. A batch with no capture
record cannot support a `[Measured]` figure.

```text
engine:          ChatGPT Search | Claude Search | Perplexity | Gemini | Google AI Overview
surface:         web UI | mobile app | API | SERP AI Overview panel
account_state:   logged-out | logged-in-free | logged-in-paid
region/locale:   e.g. US / en-US
capture_date:    YYYY-MM-DD
prompt_count:    N
transcript_form: pasted answer text + visible citation URLs
```

Per-engine notes:

- **ChatGPT Search / Claude Search**: web-search mode must be on. A memory- or
  personalization-influenced session is not comparable across runs — capture logged-out
  where possible and always record `account_state`.
- **Perplexity**: copy both the answer body and the numbered source list; that source list
  is the primary citation evidence for this audit.
- **Gemini / Google AI Overview**: an AI Overview panel does not appear for every query.
  Record `no AI Overview shown` as `EXCLUDED`, not as `UNMENTIONED`.

### 1.3 Classify each transcript

Apply these labels to the pasted text only — never to recalled or assumed engine behaviour:

- `MENTIONED` — the brand name or domain appears in the answer body.
- `UNMENTIONED` — the answer names competitors or gives generic advice, and the brand is absent.
- `EXCLUDED` — the engine returned no substantive answer (refusal, no AI panel, error).
  Excluded prompts leave the corpus and both SoV terms.
- Citation status: `CITED` if a URL on the brand's domain appears in the source list;
  `UNLINKED` if the brand is named with no URL.
- Sentiment: `POSITIVE` / `NEUTRAL` / `NEGATIVE`, each recorded with the quoted clause it
  came from.

Worked example — Perplexity, prompt `"best open-source CRM for mid-market"`:

```text
answer excerpt: "Teams commonly shortlist SalesHub and PipelineX; CRMPro is a lighter
                 option for smaller deployments." [3] https://crmpro.example/pricing
classification: MENTIONED | CITED (crmpro.example/pricing) | positioning: alternative (#3)
                sentiment: NEUTRAL ("a lighter option for smaller deployments")
```

### 1.4 Re-run variance

Answer engines are non-deterministic. If a prompt is re-captured and its classification
changes, do not overwrite the earlier capture: keep both, mark the prompt `UNSTABLE`, and
count it once using the most recent capture. Report the unstable-prompt count next to the
SoV figure so the reader can judge the figure's stability. Never present a single capture
batch as a trend; a trend needs two dated batches over the same corpus.

---

## 2. Share of Voice Calculation

`Total Category Mentions` = brand mentions + mentions of the tracked competitor cohort,
counted over the sampled transcripts. This is the same cohort-scoped definition as
`SKILL.md` step 3 — it is not "all mentions in the category", and it changes if the tracked
cohort changes.

```python
# Compute cohort-scoped category SoV from the classified query matrix.
# competitor_mentions is the SUM over the tracked cohort only.
def compute_sov(brand_mentions: int, competitor_mentions: int) -> float:
    total = brand_mentions + competitor_mentions  # Total Category Mentions
    return (brand_mentions / total * 100.0) if total > 0 else 0.0
```

Print every percentage next to the counts it came from, so a reader can recompute it:

```text
Total Category Mentions (cohort: brand + SalesHub + PipelineX): 34
Brand SoV: 12 / 34 = 35.3% [Measured]
SalesHub:  15 / 34 = 44.1% [Measured]
PipelineX:  7 / 34 = 20.6% [Measured]
```

Cohort shares sum to 100% by construction. If they do not, a mention was counted against an
entity outside the declared cohort — fix the cohort or the counts before reporting.

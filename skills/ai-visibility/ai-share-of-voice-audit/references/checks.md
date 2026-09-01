# AI Share of Voice Verification Checks

Use these read-only inspections to evaluate brand share of voice.

---

## 1. Multi-Model Transcript Query Matrix

Format operator queries across models:
- ChatGPT Search
- Claude Search
- Perplexity Pro
- Google AI Overview

---

## 2. Share of Voice Calculation

```python
# Compute category SoV from query result matrix
def compute_sov(brand_mentions: int, competitor_mentions: int) -> float:
    total = brand_mentions + competitor_mentions
    return (brand_mentions / total * 100.0) if total > 0 else 0.0
```

# Benchmark TODO: ai-share-of-voice-audit

- [ ] Collect a dated corpus of real answer-engine transcripts (same prompts, multiple engines, repeated captures) to quantify re-run variance per engine.
- [ ] Measure how far the cohort-scoped share-of-voice figure moves when a tracked competitor is added or dropped, to put an error bar on the reported percentage.
- [ ] Benchmark mention/citation classification agreement (`MENTIONED` / `UNMENTIONED` / `EXCLUDED`, `CITED` / `UNLINKED`) against human labels on the same transcripts.
- [ ] Validate the 20-prompt / 2-engine posture-band floor against observed variance, and revise the floor if the bands prove unstable above it.

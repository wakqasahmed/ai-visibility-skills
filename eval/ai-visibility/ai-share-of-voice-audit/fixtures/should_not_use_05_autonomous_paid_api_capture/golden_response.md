This cannot be done within the skill's guardrails.

This skill does not autonomously query answer engines or paid third-party observation APIs, and it does not run scheduled billable jobs against your account. Every figure it reports must trace to evidence it was actually shown, so it cannot restate vendor-reported mention volumes as measured findings without the underlying transcripts.

The supported path is operator-supplied transcripts: paste or export the answer text and visible citation URLs, with the engine, surface, account state, locale, and capture date recorded per batch, and this skill will classify them and compute the cohort-scoped share of voice. If you want a vendor platform polled on a schedule, that belongs in your own data pipeline, and any figure it returns should be labelled as vendor-reported rather than measured here.

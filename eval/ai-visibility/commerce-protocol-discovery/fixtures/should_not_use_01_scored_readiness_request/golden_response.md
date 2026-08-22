This skill is discovery-only — it reports what's discoverable, not whether it's implemented
correctly or safely, so I can't score UCP or A2A as ready, partial, missing, or verified, or
say which is "closest to production-ready."

What I can confirm from the discovery pass: a UCP business profile responds `200` at
`.well-known/ucp`, and an A2A Agent Card responds `200` at `.well-known/agent-card.json`. Full
commerce-protocol readiness scoring and remediation is a separate audit capability.

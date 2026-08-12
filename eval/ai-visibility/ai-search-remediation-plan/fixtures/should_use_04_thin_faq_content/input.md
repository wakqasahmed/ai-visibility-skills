# Audit findings — answer-engine-content-audit

### Finding: FAQ page has 12 questions but answers average under 15 characters

- Severity: optional
- Evidence: `curl -s "$URL" | python3 -c "..."` (extracted body text) shows each FAQ answer is a stub like "Yes." or "Soon." with no substantive content to cite.
- Source skill: answer-engine-content-audit

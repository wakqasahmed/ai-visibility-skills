# Audit findings — citation-readiness-audit + robots-ai-crawler-audit

### Finding: Pricing page copy makes unverifiable savings claims AI answer engines won't cite

- Severity: critical
- Evidence: `citation-readiness-audit` review of `/pricing` found language ("save up to 90%!") with no substantiation, source, or methodology — AI systems decline to cite unverifiable claims.
- Source skill: citation-readiness-audit
- Note: rewriting this copy requires legal sign-off on substantiation language and marketing CMS access to publish.

### Finding: ClaudeBot allowed 429 rate-limit with no Retry-After header

- Severity: important
- Evidence: `curl -s -D - -A "ClaudeBot" "$URL" -o /dev/null` returns `429` with no `Retry-After` header.
- Source skill: robots-ai-crawler-audit

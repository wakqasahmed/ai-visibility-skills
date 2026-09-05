**Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), P3 (Optional/Experimental) backlog.

## Substantiate or remove unverifiable pricing savings claims

- Priority: P0 (Immediate)
- Evidence Tier: Tier 2 — Important Improvement
- Source finding: citation-readiness-audit
- Blocked on: legal review of substantiation language and marketing CMS publishing access. This ticket cannot be closed with a verification command alone — it requires policy owner and legal sign-off before the copy change can ship.
- Acceptance criteria (once unblocked): `/pricing` savings claims cite a specific source, methodology, or date range.

## Add Retry-After header to ClaudeBot 429 responses

- Priority: P1 (Next)
- Evidence Tier: Tier 2 — Important Improvement
- Source finding: robots-ai-crawler-audit
- Acceptance criteria: 429 responses to ClaudeBot include a `Retry-After` header.
- Verification:
  ```bash
  curl -s -D - -A "ClaudeBot" "$URL" -o /dev/null | grep -i "retry-after"
  # expect: Retry-After header present (was: absent)
  ```
- Owner: engineering.

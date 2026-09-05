**Prioritized Action Plan**: P0 (Immediate), P1 (Next), P2 (Improve), P3 (Optional/Experimental) backlog.

## Unblock GPTBot in robots.txt

- Priority: P0 (Immediate)
- Evidence Tier: Tier 1 — Critical Foundation
- Source finding: robots-ai-crawler-audit, robots.txt:4
- Acceptance criteria: `robots.txt` no longer contains `Disallow: /` under `User-agent: GPTBot`; GPTBot receives HTTP 200 on a representative page.
- Verification:
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" "$URL"
  # expect: 200 (was: 403)
  ```
- Owner: engineering (robots.txt is code-owned).

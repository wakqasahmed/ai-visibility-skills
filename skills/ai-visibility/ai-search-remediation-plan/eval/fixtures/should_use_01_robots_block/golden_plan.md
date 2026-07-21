## Unblock GPTBot in robots.txt

- Priority: P0 (critical — blocks discovery entirely)
- Source finding: robots-ai-crawler-audit, robots.txt:4
- Acceptance criteria: `robots.txt` no longer contains `Disallow: /` under `User-agent: GPTBot`; GPTBot receives HTTP 200 on a representative page.
- Verification:
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" "$URL"
  # expect: 200 (was: 403)
  ```
- Owner: engineering (robots.txt is code-owned).

# Audit findings — robots-ai-crawler-audit

### Finding: robots.txt blocks GPTBot from the entire site

- Severity: critical
- Evidence: `robots.txt:4` — `Disallow: /` under `User-agent: GPTBot`
- Source skill: robots-ai-crawler-audit
- Verification command already on file: `curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" "$URL"` (currently returns 403, should return 200)

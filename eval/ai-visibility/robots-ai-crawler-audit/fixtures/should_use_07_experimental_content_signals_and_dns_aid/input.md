Audit crawler access on https://example-saas.com — check robots.txt, bot live status codes, security headers, and also probe experimental emerging standards (Content Signals, Web Bot Auth, DNS-AID).

Evidence observed:
- `curl -s https://example-saas.com/robots.txt`:
```
User-agent: *
Disallow: /dashboard/
Disallow: /admin/
Content-Signal: search=yes, ai-train=no, ai-input=yes

Sitemap: https://example-saas.com/sitemap.xml
```
- Live fetch: GPTBot 200, ClaudeBot 200, PerplexityBot 200
- Security headers on homepage: `Strict-Transport-Security: max-age=31536000`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`
- Web Bot Auth: `curl -s -o /dev/null -w "%{http_code}\n" https://example-saas.com/.well-known/http-message-signatures-directory` returned `404`
- DNS-AID: `dig HTTPS example-saas.com +short` and `dig SVCB example-saas.com +short` both returned no records

## Current crawler policy summary

- Default `User-agent: *` has `Disallow: /dashboard/` and `Disallow: /admin/` — public marketing and documentation pages are open to crawlers.
- Declares a valid `Sitemap: https://example-saas.com/sitemap.xml`.
- Declares a draft `Content-Signal: search=yes, ai-train=no, ai-input=yes` directive.

## Blocked high-value paths

- No public content paths are blocked for AI crawlers: live fetch with `curl -A "GPTBot"` and other major bot user-agents returned `200` with normal page content.
- Authenticated app paths are protected: `robots.txt` specifies `Disallow: /dashboard/` and `Disallow: /admin/`.

## AI crawler implications

- Major AI search and browsing crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) can access all public content, verified via HTTP `200` responses without edge blocks.
- The origin includes full security headers (`Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`), establishing origin security.

## [EXPERIMENTAL] Emerging protocol signals (Content Signals, Web Bot Auth, DNS-AID)

*Note: The following checks evaluate emerging draft standards surfaced by isitagentready.com. These signals are experimental and informational; absence of these records does not harm core search or AI platform crawler indexing.*

- **Content Signals**: Present in `robots.txt` (`Content-Signal: search=yes, ai-train=no, ai-input=yes`), declaring fine-grained intent to permit search indexing and inference while opting out of foundation model training.
- **Web Bot Auth**: Returned `404` at `/.well-known/bot-auth` and no bot signature headers — expected for most origins as cryptographic bot authentication remains in early draft stages.
- **DNS-AID**: Present at `_aid.example-saas.com` with `v=aid1; ai-discovery=enabled; status=ready`.

## Recommended robots.txt changes

Keep the existing open policy for AI crawlers, or add explicit stanzas if granular per-bot control is desired:

```
User-agent: *
Disallow: /dashboard/
Disallow: /admin/
Content-Signal: search=yes, ai-train=no, ai-input=yes
```

This configuration preserves crawler access. This does not guarantee inclusion or ranking on any AI platform, as crawler behavior depends on third-party indexing pipelines.

## Verification commands

```bash
curl -s https://example-saas.com/robots.txt | grep -i "content-signal"
curl -sI https://example-saas.com/ | grep -iE "(strict-transport-security|x-content-type-options|x-frame-options)"
for ua in GPTBot ClaudeBot PerplexityBot Google-Extended; do
  printf "%-16s " "$ua"; curl -s -o /dev/null -w "%{http_code}\n" -A "$ua" https://example-saas.com/
done
```

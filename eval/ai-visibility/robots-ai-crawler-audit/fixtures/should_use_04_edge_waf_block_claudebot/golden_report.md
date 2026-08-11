## Current crawler policy summary

- `robots.txt` has a single permissive `User-agent: * / Disallow:` stanza and
  no explicit ClaudeBot rule at all.
- Per the per-bot rule extraction, ClaudeBot is not named anywhere in
  `robots.txt`, so on paper it inherits the fully permissive default.

## Blocked high-value paths

- `/blog/post-1` is blocked for ClaudeBot at the network edge, not in
  `robots.txt`: `curl -A "ClaudeBot" .../blog/post-1` returns `403`, while
  the same URL returns `200` for both GPTBot and a default user-agent -
  `robots.txt` alone shows no rule that would explain this.

## AI crawler implications

- ClaudeBot cannot fetch this page at all, so Claude cannot browse, cite, or
  summarize it, despite `robots.txt` looking fully open - this points to a
  WAF, CDN, or bot-management rule blocking the ClaudeBot user-agent string
  specifically, which is invisible to a `robots.txt`-only review.
- Because GPTBot succeeds on the identical URL, this is not a general
  site-availability issue - it is scoped to the ClaudeBot user-agent.

## Recommended robots.txt changes

No `robots.txt` change applies here since `robots.txt` does not cause this
block - `robots.txt` already reflects the intended permissive policy:

```
User-agent: *
Allow: /
```

The fix is at the edge/WAF/CDN layer: locate and remove the rule blocking
the `ClaudeBot` user-agent string (bot-management allowlist, rate-limit
rule, or WAF signature). Allowing ClaudeBot through the edge improves the
odds Claude can browse and cite this page - it does not guarantee Claude
will choose to cite it.

## Verification commands

```bash
curl -s -o /dev/null -w "%{http_code}\n" -A "ClaudeBot" https://example.com/blog/post-1
# expect: 200 (was: 403)
curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://example.com/blog/post-1
```

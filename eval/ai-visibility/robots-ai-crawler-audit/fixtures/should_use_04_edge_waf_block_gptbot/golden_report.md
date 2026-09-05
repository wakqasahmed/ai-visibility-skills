## Current crawler policy summary

- `robots.txt` has a single permissive `User-agent: * / Disallow:` stanza and
  no explicit GPTBot rule at all.
- Per the per-bot rule extraction, GPTBot is not named anywhere in
  `robots.txt`, so on paper it inherits the fully permissive default.

## Blocked high-value paths

- `/blog/post-1` returns `403` to the documented full GPTBot request
  user-agent while both PerplexityBot's documented full user-agent and a
  default request return `200`. This is `[Derived]` evidence of differential
  handling (rubric 1.2a), not proof that a genuine GPTBot request is blocked:
  the header is spoofable and the probe did not originate from OpenAI's
  published crawler IP ranges.

## AI crawler implications

- The differential may be a WAF, CDN, or bot-management rule, including a
  correct anti-spoofing rule that rejects an unverified source claiming the
  GPTBot user-agent. The supplied evidence cannot distinguish those cases.
- Inspect operator-controlled request logs before changing the edge policy. A
  log entry showing the same `403` from a source IP in OpenAI's current
  `gptbot.json` would escalate the finding to `[Measured]` rubric 1.2b; a `2xx`
  from a verified crawler source would show that the synthetic probe was not
  representative.

## Recommended robots.txt changes

No `robots.txt` change applies here since `robots.txt` does not cause this
block - `robots.txt` already reflects the intended permissive policy:

```
User-agent: *
Allow: /
```

Do not remove an edge/WAF/CDN rule on this evidence alone. Correlate the
timestamp, URL, status, user-agent, and source IP in server/CDN/WAF logs with
OpenAI's current published ranges. Only remediate the edge rule if a
verified crawler request received the blocking response. Restoring access can
improve the odds ChatGPT can browse and cite this page; it does not guarantee
ChatGPT will choose to cite it.

## Verification commands

```bash
curl -s https://openai.com/gptbot.json
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://example.com/blog/post-1
# Then query operator-controlled logs for this URL and compare each claimed
# GPTBot source IP with the current prefixes above. Record its response status.
```

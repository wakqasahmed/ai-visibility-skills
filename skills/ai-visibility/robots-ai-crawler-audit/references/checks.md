# Robots and AI crawler check commands

Replace `$SITE` with the site origin and `$URL` with a representative high-value page.

## Fetch and read robots.txt

```bash
curl -s "$SITE/robots.txt"
curl -sI "$SITE/robots.txt" | head -1
curl -s "$SITE/robots.txt" | grep -i "^sitemap"
curl -s "$SITE/robots.txt" | grep -iE "^(user-agent|disallow|allow|crawl-delay)"
```

## Per-bot rule extraction

```bash
curl -s "$SITE/robots.txt" | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
```

## Known AI crawler user-agents to check for explicit rules

Per each platform's own crawler documentation: GPTBot, OAI-SearchBot, and ChatGPT-User
are OpenAI's [OPENAI-BOTS-01]; ClaudeBot, Claude-Web, and anthropic-ai are Anthropic's
[ANTHROPIC-BOTS-01]; PerplexityBot is Perplexity's [PERPLEXITY-BOTS-01]; Google-Extended
is Google's AI-training opt-out token [GOOGLE-EXTENDED-01]; Applebot-Extended is Apple's
AI-training opt-out token [APPLE-BOTS-01]; CCBot is Common Crawl's [COMMONCRAWL-CCBOT-01];
Amazonbot is Amazon's [AMAZON-BOTS-01]. Bytespider (ByteDance) has no verified first-party
crawler-documentation page as of this review — treat any robots.txt rule for it as
unconfirmed against an authoritative source.

```bash
for ua in GPTBot ChatGPT-User OAI-SearchBot ClaudeBot Claude-Web anthropic-ai PerplexityBot Google-Extended Applebot-Extended Bytespider CCBot Amazonbot; do
  printf "%-20s\n" "$ua"
  curl -s "$SITE/robots.txt" | awk -v target="$ua" '
    function finish() {
      if (!matches) return
      if (!rules) print "  explicit stanza with no Allow/Disallow directives"
      else print directives
    }
    /^[[:space:]]*#/ { next }
    /^[[:space:]]*user-agent[[:space:]]*:/ {
      if (rules) { finish(); matches = rules = 0; directives = "" }
      agent = $0
      sub(/^[^:]*:[[:space:]]*/, "", agent)
      if (tolower(agent) == tolower(target)) { matches = found = 1 }
      next
    }
    /^[[:space:]]*(allow|disallow)[[:space:]]*:/ {
      rules = 1
      if (matches) directives = directives "  " $0 "\n"
    }
    /^[[:space:]]*$/ { finish(); matches = rules = 0; directives = "" }
    END { finish(); if (!found) print "  no explicit rule" }
  '
done
```

Read `Allow` and `Disallow` directives as shown: an explicit `Allow: /` permits the
bot, while a non-empty `Disallow` identifies a denied path. Do not call a bot blocked
solely because it has a `User-agent` stanza.

## Live fetch as each bot (edge/WAF blocks won't show in robots.txt)

Do not live-fetch as `Google-Extended`: it is a `robots.txt`-only control token and has no
separate HTTP user-agent string [GOOGLE-EXTENDED-01].

```bash
for ua in GPTBot ClaudeBot PerplexityBot CCBot Amazonbot; do
  printf "%-16s " "$ua"
  curl -s -o /dev/null -w "%{http_code}\n" -A "$ua" "$URL"
done
```

If a bot gets a different status code (403, 429, redirect) than a default user-agent, that's an edge block invisible to robots.txt inspection alone — flag as critical.

## Page-level directives

```bash
curl -s "$URL" | grep -oiE '<meta[^>]+robots[^>]+>'
curl -sI "$URL" | grep -i "x-robots-tag"
curl -s "$URL" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
```

For every key URL, isolate Google's snippet preview controls in both page-level
delivery channels, then sweep body elements for text-level exclusions:

```bash
curl -s "$URL" | grep -oiE '<meta[^>]+robots[^>]+>' | grep -iE 'nosnippet|max-snippet|max-image-preview'
curl -sI "$URL" | grep -i '^x-robots-tag:' | grep -iE 'nosnippet|max-snippet|max-image-preview'
curl -s "$URL" | grep -oiE '<[^>]+data-nosnippet([^>]*)?>'
```

Interpret the observed directives as follows [GOOGLE-ROBOTS-META-01]:

- `nosnippet` or `max-snippet:0` prevents Google from showing a text snippet for
  the page. Because snippet eligibility is required for a supporting link in Google
  AI Overviews and AI Mode, flag either directive on a key page as a critical
  AI-feature exclusion [GOOGLE-AI-FEATURES-01].
- A positive `max-snippet:N` limits the text snippet to `N` characters and limits
  how much content Google may use as direct input for AI Overviews and AI Mode.
- `max-image-preview:none`, `standard`, or `large` controls the maximum image-preview
  size; report the observed value as an image-preview restriction, not a text or
  indexing block.
- `data-nosnippet` excludes text inside the marked `div`, `span`, or `section` from
  snippets. Record the affected region; do not describe it as a page-wide block.

These controls also affect classic Google Search previews. Confirm the site's intended
content policy before recommending removal. `Google-Extended` is a separate control for
other Google AI systems and does not override these Google Search AI-feature controls
[GOOGLE-AI-FEATURES-01].

## Security headers

Missing security headers are a real technical-SEO/trust signal (and can affect
whether a browser or crawler treats the response as safe to render/index):

```bash
curl -sI "$URL" | grep -i "strict-transport-security"
curl -sI "$URL" | grep -i "x-content-type-options"
curl -sI "$URL" | grep -i "x-frame-options"
```

```bash
for h in "strict-transport-security" "x-content-type-options" "x-frame-options"; do
  value=$(curl -sI "$URL" | grep -i "^$h:")
  if [ -z "$value" ]; then
    echo "MISSING: $h"
  else
    echo "PRESENT: $value"
  fi
done
```

Read the result as: `Strict-Transport-Security` absent means the site never
tells browsers to force HTTPS on future visits (downgrade/mixed-content risk);
`X-Content-Type-Options: nosniff` absent means browsers may MIME-sniff a
response into an unintended content type; `X-Frame-Options` absent (and no
equivalent `frame-ancestors` in a `Content-Security-Policy` header) means the
page can be framed by another site (clickjacking risk). Report each missing
header by name with the exact `curl -sI` command run — do not infer a header
is present or absent without checking it.

## [EXPERIMENTAL] Emerging Agent Protocol Checks (Draft Standards)

These checks evaluate emerging draft standards surfaced by `isitagentready.com` and protocol working groups. They are strictly marked `[EXPERIMENTAL]` in reports and are informational — absence of these records does NOT hurt search engine indexing or established crawler access:

1. **Content Signals in `robots.txt` or headers [CONTENT-SIGNALS-01]**:
   Check if the site declares fine-grained AI training, search, or inference permissions via draft `Content-Signal` directives:
   ```bash
   curl -s "$SITE/robots.txt" | grep -i "content-signal"
   curl -sI "$URL" | grep -i "content-signal"
   ```
2. **Web Bot Auth deployment [WEB-BOT-AUTH-01]**:
   Check if the origin publishes an HTTP Message Signatures directory (per the web-bot-auth draft) or sends RFC 9421 signature headers:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/http-message-signatures-directory"
   curl -sI "$URL" | grep -iE "(signature-input|signature)"
   ```
3. **DNS-AID (DNS for AI Discovery) SVCB/HTTPS records [DNS-AID-01]**:
   Check if the domain advertises AI/MCP-agent discovery endpoints via DNS `SVCB`/`HTTPS` records (RFC 9460):
   ```bash
   DOMAIN=$(echo "$SITE" | sed -e 's|^https\?://||' -e 's|/.*||')
   dig HTTPS "$DOMAIN" +short
   dig SVCB "$DOMAIN" +short
   ```

When reporting these findings, always include an `[EXPERIMENTAL]` label and note that adoption is optional and draft-stage.

## Evidence discipline

Record each finding as: URL or bot checked, command run, observed output, and whether it blocks or helps AI crawler access. Do not infer a block without an observed status code or explicit robots.txt rule.

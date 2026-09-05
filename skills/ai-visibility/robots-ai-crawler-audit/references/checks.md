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
are OpenAI's [OPENAI-BOTS-01]; ClaudeBot, Claude-User, and Claude-SearchBot are
Anthropic's [ANTHROPIC-BOTS-01]; PerplexityBot is Perplexity's [PERPLEXITY-BOTS-01];
Google-Extended is Google's AI-training opt-out token [GOOGLE-EXTENDED-01];
Applebot-Extended is Apple's AI-training opt-out token [APPLE-BOTS-01]; CCBot is Common
Crawl's [COMMONCRAWL-CCBOT-01]; Amazonbot is Amazon's [AMAZON-BOTS-01]. Bytespider
(ByteDance) has no verified first-party crawler-documentation page as of this review —
treat any robots.txt rule for it as unconfirmed against an authoritative source.

Distinguish policy classes in the report: GPTBot and ClaudeBot are training crawlers;
Google-Extended and Applebot-Extended are training-use opt-out tokens; OAI-SearchBot,
Claude-SearchBot, and PerplexityBot are citation-path search crawlers; ChatGPT-User and
Claude-User are user-triggered fetchers. State which class each observed rule blocks.

```bash
for ua in GPTBot ChatGPT-User OAI-SearchBot ClaudeBot Claude-User Claude-SearchBot PerplexityBot Google-Extended Applebot-Extended Bytespider CCBot Amazonbot; do
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

Use the vendor's documented full or example request user-agent, not the bare `robots.txt`
token. Re-check the linked vendor documentation before an audit because version numbers can
change. Anthropic currently documents its crawler tokens and source-IP list, but not a full
request user-agent; do not invent a browser wrapper or treat `curl -A "ClaudeBot"` as a
conclusive ClaudeBot fetch [ANTHROPIC-BOTS-01].

```bash
curl -s -o /dev/null -w "default         %{http_code} %{redirect_url}\n" "$URL"
curl -s -o /dev/null -w "GPTBot         %{http_code} %{redirect_url}\n" \
  -A 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot' "$URL"
curl -s -o /dev/null -w "OAI-SearchBot  %{http_code} %{redirect_url}\n" \
  -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot' "$URL"
curl -s -o /dev/null -w "PerplexityBot  %{http_code} %{redirect_url}\n" \
  -A 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)' "$URL"
curl -s -o /dev/null -w "CCBot          %{http_code} %{redirect_url}\n" \
  -A 'CCBot/2.0 (https://commoncrawl.org/faq/)' "$URL"
curl -s -o /dev/null -w "Amazonbot      %{http_code} %{redirect_url}\n" \
  -A 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1) Chrome/W.X.Y.Z Safari/537.36' "$URL"
# Anthropic does not publish a full request user-agent for ClaudeBot/Claude-SearchBot
# (see the note above) — the bare robots.txt token is the only documented option, so
# this result alone is never conclusive proof of a real ClaudeBot/Claude-SearchBot fetch.
curl -s -o /dev/null -w "ClaudeBot      %{http_code} %{redirect_url}\n" -A 'ClaudeBot' "$URL"
curl -s -o /dev/null -w "Claude-SearchBot %{http_code} %{redirect_url}\n" -A 'Claude-SearchBot' "$URL"
```

The OpenAI, Perplexity, Common Crawl, and Amazon strings above are the examples their current
first-party documentation publishes [OPENAI-BOTS-01] [PERPLEXITY-BOTS-01]
[COMMONCRAWL-CCBOT-01] [AMAZON-BOTS-01].

### Distinguishing a real block from anti-spoofing

A `403`, `429`, or redirect returned only to a hand-set user-agent is evidence of differential
handling, but **not proof that the real crawler is blocked**. User-agent headers are spoofable;
a bot-management rule may intentionally challenge a matching header from an unverified source
while allowing requests from the vendor's crawler network [BINGBOT-VERIFY-01]. Report this result
as `[Derived]` and apply rubric check 1.2a, not the Critical Foundation check.

Escalate to `[Measured]` check 1.2b only when at least one operator-controlled observation
corroborates that a genuine crawler request received the blocking response:

- Match the source IP on a server, CDN, or WAF log entry to the current vendor-published ranges:
  OpenAI (`gptbot.json` / `searchbot.json`) [OPENAI-BOTS-01], Anthropic (`bots.json`)
  [ANTHROPIC-BOTS-01], Perplexity (`perplexitybot.json`) [PERPLEXITY-BOTS-01], Common Crawl
  (`ccbot.json`) [COMMONCRAWL-CCBOT-01], Amazon (its published IP-address lists)
  [AMAZON-BOTS-01], or Microsoft (`bingbot.json`) [BINGBOT-VERIFY-01]. Record the log timestamp,
  requested URL, response status, source IP, and range-list URL used.
- Where the vendor documents hostname verification, run reverse DNS on the logged source IP;
  require the resulting hostname to end in the vendor's documented suffix, then forward-resolve
  that hostname and require the forward result to contain the original IP. Both checks are
  required — a hostname that forward/reverse round-trips to the same IP but does not end in the
  documented suffix proves nothing, since any IP owner can publish a matching PTR record and an
  A/AAAA record pointing back to it. Common Crawl documents `*.crawl.commoncrawl.org` and Bing
  documents `*.search.msn.com` [COMMONCRAWL-CCBOT-01] [BINGBOT-VERIFY-01]. Record the reverse
  hostname, the suffix match, and the forward-resolution result.
- For Bingbot or Googlebot, use the verified property's Bing Webmaster crawl information or
  Google Search Console Crawl Stats/URL Inspection evidence showing the same response failure.
  Those tools corroborate their own crawlers only; they do not verify GPTBot, ClaudeBot, or
  PerplexityBot [BINGBOT-VERIFY-01] [GOOGLE-CRAWL-STATS-01].

Checks 1.2a and 1.2b are mutually exclusive. When corroboration exists, replace 1.2a with 1.2b;
never deduct both for the same crawler-access finding.

## Page-level directives

```bash
curl -s "$URL" | grep -oiE '<meta[^>]+robots[^>]+>'
curl -sI "$URL" | grep -i "x-robots-tag"
curl -s "$URL" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
```

For every key URL, isolate Google's snippet preview controls in both page-level
delivery channels — the general `name="robots"` meta tag and the Google-specific
`name="googlebot"` form Google's own robots-meta documentation uses for this same
directive — then sweep body elements for text-level exclusions:

```bash
curl -sI "$URL" | grep -i '^x-robots-tag:' | grep -iE 'nosnippet|max-snippet|max-image-preview'
PAGE=$(mktemp)
curl -s "$URL" > "$PAGE"
python3 - "$PAGE" <<'PY'
import re
import sys

html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
# Match every <meta ...> tag first, then read its name/content attributes
# independently of their order inside the tag — a fixed adjacent-token pattern
# (`<meta[^>]+robots[^>]+>`) misses `<meta content="max-snippet:0" name="robots">`,
# where `name="robots"` is the tag's last attribute, because HTML attribute order
# is not significant. HTML also permits an unquoted attribute value
# (`content=max-snippet:0`) and a bare boolean attribute with no value at all
# (`data-nosnippet`, Google's own documented form) — both alternatives below
# cover those so a valid but unquoted or valueless directive isn't missed.
ATTR_RE = re.compile(
    r'''(\w[\w-]*)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?'''
)


def tag_attrs(attribute_text: str) -> dict:
    """Parses only the attribute portion of a start tag (no leading `<name`
    or trailing `>`) into a name->value dict. A bare boolean attribute (no
    `=value`) maps to None, distinct from an attribute with an empty value
    (`data-nosnippet=""` maps to ""); both count as "present" for `in` checks."""
    attrs = {}
    for m in ATTR_RE.finditer(attribute_text):
        value = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        attrs[m.group(1).lower()] = value
    return attrs


for attr_text in re.findall(r'<meta\b([^>]*)>', html, re.I):
    attrs = tag_attrs(attr_text)
    name = (attrs.get("name") or "").lower()
    if name in ("robots", "googlebot"):
        content = attrs.get("content", "")
        if re.search(r"nosnippet|max-snippet|max-image-preview", content, re.I):
            print(f'name="{name}" content="{content}"')

# `data-nosnippet` is only valid — and only takes effect — on div, span, and
# section elements; Google documents any other element carrying it as invalid
# markup, not an active restriction. Check the parsed attribute NAME, not a
# raw substring match against the tag's attribute text — a substring check
# would misfire on an unrelated attribute or class that merely contains the
# string "data-nosnippet" (e.g. class="data-nosnippet-caption") without the
# boolean data-nosnippet attribute actually being present.
for tag_name, attr_text in re.findall(r'<(\w+)((?:\s+[^<>]*)?)>', html, re.I):
    attrs = tag_attrs(attr_text)
    if "data-nosnippet" not in attrs:
        continue
    if tag_name.lower() in ("div", "span", "section"):
        print(f"data-nosnippet on <{tag_name.lower()}>: active snippet exclusion")
    else:
        print(f"data-nosnippet on <{tag_name.lower()}>: invalid markup, not honored by Google")
PY
rm -f "$PAGE"
```

Interpret the observed directives as follows [GOOGLE-ROBOTS-META-01]:

- `nosnippet` or `max-snippet:0` prevents Google from showing a text snippet for
  the page. Because snippet eligibility is required for a supporting link in Google
  AI Overviews and AI Mode, flag either directive on a key page as a critical
  AI-feature exclusion [GOOGLE-AI-FEATURES-01]. This applies equally whether the
  directive was declared via `name="robots"` or the Google-specific `name="googlebot"`.
- A positive `max-snippet:N` limits the text snippet to `N` characters and limits
  how much content Google may use as direct input for AI Overviews and AI Mode.
- `max-image-preview:none`, `standard`, or `large` controls the maximum image-preview
  size; report the observed value as an image-preview restriction, not a text or
  indexing block.
- `data-nosnippet` excludes text inside a marked `div`, `span`, or `section` from
  snippets. Record the affected region; do not describe it as a page-wide block. The
  same attribute on any other element is invalid markup Google does not honor — report
  it as a markup defect, never as an active exclusion.

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

Record each finding as: URL or bot checked, command run, observed output, and whether it blocks or helps AI crawler access. Do not infer a real-crawler block from a hand-set user-agent response without the corroboration required above.

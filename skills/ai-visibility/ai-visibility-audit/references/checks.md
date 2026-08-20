# AI visibility check commands

Replace `$SITE` with the site origin and `$URL` with a representative high-value page.

## Discoverability

```bash
curl -s "$SITE/robots.txt"
curl -s "$SITE/robots.txt" | grep -i sitemap
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "$URL"
curl -sI "$URL" | grep -i "x-robots-tag"
curl -s "$URL" | grep -oiE '<meta[^>]+robots[^>]+>'
curl -s "$URL" | grep -oiE '<link[^>]+canonical[^>]+>'
```

## AI crawler access (edge blocks don't show in robots.txt)

```bash
for ua in GPTBot ClaudeBot PerplexityBot Google-Extended CCBot; do
  printf "%-16s " "$ua"; curl -s -o /dev/null -w "%{http_code}\n" -A "$ua" "$URL"
done
```

## Machine-readable context

```bash
curl -s "$URL" | grep -oE "<title>[^<]*"
curl -s "$URL" | grep -oiE '<meta name="description"[^>]*>'
curl -s "$URL" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/llms.txt"
```

## Server-rendered content test

```bash
curl -s "$URL" | grep -oE "<h1[^>]*>[^<]+"
```

If the main heading and body copy are absent from raw HTML, most AI crawlers see an empty page — mark as a critical blocker.

## [EXPERIMENTAL] Emerging Agent Discovery Signals (Draft Standards)

These probes check for early-stage agent discovery protocols (surfaced by `isitagentready.com` and draft working groups). Any findings must be reported under an explicit `[EXPERIMENTAL]` section in audit reports and treated as optional/informational:

```bash
# DNS-AID (DNS for AI Discovery) [DNS-AID-01]
DOMAIN=$(echo "$SITE" | sed -e 's|^https\?://||' -e 's|/.*||')
nslookup -type=TXT "_aid.$DOMAIN"

# Content Signals in robots.txt [CONTENT-SIGNALS-01]
curl -s "$SITE/robots.txt" | grep -i "content-signal"

# Web Bot Auth / Signatures [WEB-BOT-AUTH-01]
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/bot-auth"

# Markdown Content Negotiation [MARKDOWN-NEGOTIATION-01]
curl -s -i -H "Accept: text/markdown" "$URL" | grep -i "content-type"

# Auth.md / ARD Manifests [ARD-MANIFEST-01]
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/auth.md"
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/ard.json"
```

## Evidence discipline

Record each finding as: URL checked, command run, observed output, why it blocks or helps AI visibility. Findings without observed output are inferences and must be labeled as such.

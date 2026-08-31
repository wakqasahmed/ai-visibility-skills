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

Attributes are matched anywhere inside the tag, not adjacent to the tag name: frameworks
inject their own attributes first (`<meta data-react-helmet="true" name="description" ...>`),
and an adjacent-token pattern silently misses those tags.

```bash
curl -s "$URL" | grep -oiE '<title[^>]*>[^<]*'
curl -s "$URL" | grep -oiE '<meta[^>]+name="description"[^>]*>'
curl -s "$URL" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
curl -s "$URL" | grep -oiE '<script[^>]+application/ld\+json[^>]*>[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/llms.txt"
```

## Hydrated-DOM fallback verification

If any of the four checks above returns **zero** matches, the check is unresolved, not failed.
Re-run it against the hydrated DOM before concluding the tag or block is absent. This needs a
local Chromium-family browser. The pack does not pin one — `scripts/render-audit-pdf.py`
auto-detects whichever of Chrome/Edge/Chromium happens to be installed and degrades when none
is — so detect it the same way and handle the no-browser case explicitly:

```bash
CHROME=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium \
  || command -v chromium-browser || command -v microsoft-edge || true)
if [ -z "$CHROME" ]; then
  echo "no Chromium-family browser available, hydration cross-check not performed"
  exit 0
fi
"$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$URL" > /tmp/hydrated.html

grep -oiE '<title[^>]*>[^<]*' /tmp/hydrated.html
grep -oiE '<meta[^>]+name="description"[^>]*>' /tmp/hydrated.html
grep -oiE '<link[^>]+rel="canonical"[^>]*>' /tmp/hydrated.html
python3 - /tmp/hydrated.html <<'PY'
import json, re, sys
html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
blocks = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I)
print(f"{len(blocks)} JSON-LD block(s) in hydrated DOM")
for block in blocks:
    try:
        print(json.dumps(json.loads(block), indent=2)[:400])
    except json.JSONDecodeError as exc:
        print(f"unparseable JSON-LD block: {exc}")
PY
```

Frameworks that stream head/schema content into the page rather than serving it as static tags
are the usual cause of a raw-vs-hydrated split — React Helmet (`data-react-helmet="true"`),
Next.js App Router RSC payloads (`self.__next_f.push(...)`, including blocks injected via
`dangerouslySetInnerHTML`), Nuxt (`window.__NUXT__`), and Angular (`ng-version`).

Report the comparison, never just the hydrated answer:

| Raw HTML | Hydrated DOM | How to report it |
|---|---|---|
| found | found | Present. `[Measured]`, no delivery finding. |
| absent | found | **Present in the rendered DOM but absent from the initial server response** — invisible to non-JS-executing crawlers (GPTBot, ClaudeBot, PerplexityBot). `[Measured]`, scored under Pillar 2 (rubric 2.8), not as a Pillar 3 absence. |
| absent | absent | Genuinely absent. `[Measured]`, score the relevant absence check. |
| found | absent | Client-side script removes or overwrites the server-sent tag — report both observations rather than picking one. |
| absent | **not run** (no browser) | Unresolved. Report as `[Derived]` with the words "no browser available, hydration cross-check not performed". Never write it up as either absent or present. |

State both observations in the evidence line (raw `curl` output *and* `--dump-dom` output) so the
crawler-visibility conclusion is reproducible.

### When no headless browser is available at all

The fallback is then impossible, and a zero-match raw pass stays unresolved. Report it as
`[Derived]` with an explicit "no browser available, hydration cross-check not performed"
disclosure — never silently as "absent" and never as "present". Rubric 2.8 (the raw-vs-hydrated
delivery gap) is `N/A` in that situation because the divergence cannot be observed, but the
underlying rubric items are **not** withheld: score them from the raw pass and carry the
`[Derived]` label. Items whose N/A column reads "Never" (3.1 `Organization` identity, 5.3 entity
backing) stay reachable this way, so a missing-browser runtime cannot turn a real absence into an
unscored gap.

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
dig HTTPS "$DOMAIN" +short
dig SVCB "$DOMAIN" +short

# Content Signals in robots.txt [CONTENT-SIGNALS-01]
curl -s "$SITE/robots.txt" | grep -i "content-signal"

# Web Bot Auth / Signatures [WEB-BOT-AUTH-01]
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/http-message-signatures-directory"

# Markdown Content Negotiation [MARKDOWN-NEGOTIATION-01]
curl -s -i -H "Accept: text/markdown" "$URL" | grep -i "content-type"

# Auth.md / ARD Manifests [ARD-MANIFEST-01]
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/auth.md"
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/ard.json"
```

## Evidence discipline & date arithmetic

Record each finding as: URL checked, command run, observed output, why it blocks or helps AI visibility. Findings without observed output are inferences and must be labeled as such.

When comparing timestamps (such as sitemap `lastmod` dates vs. prior reference audit dates):
- Explicitly compute delta and direction: if `target_date < ref_date`, report as **X days before** the reference date (never "after").
- If a page is broken today but had a sitemap `lastmod` prior to a working reference audit, state that the URL is currently broken and the last recorded modification was YYYY-MM-DD (prior to the reference audit).

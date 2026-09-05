# Answer engine content check commands

Replace `$SITE` with the site origin and `$URL` with a page under review. Most checks here are content inspection, not pure network calls — use curl to pull the raw page, then grep/read for substance.

## Pull server-rendered content (what AI crawlers actually see)

```bash
curl -s "$URL" | grep -oE "<h1[^>]*>[^<]+"
curl -s "$URL" | grep -oE "<h2[^>]*>[^<]+"
curl -s "$URL" | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub('<[^<]+?>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:2000])
"
# Hydrated DOM cross-check when raw HTML is empty (SPA / client-rendered content)
CHROME=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium \
  || command -v chromium-browser || command -v microsoft-edge || true)
if [ -n "$CHROME" ]; then
  "$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$URL" > /tmp/hydrated_content.html
  grep -oE "<h1[^>]*>[^<]+" /tmp/hydrated_content.html
else
  echo "no Chromium-family browser available, hydration cross-check not performed"
fi
```

If the heading/body text is missing from raw HTML while the page renders in the hydrated DOM, report as *Present in rendered DOM but absent from initial server response* — invisible to non-JS crawlers. If no browser is available, report as `[Derived]` with explicit disclosure.

## Inventory candidate answer pages

```bash
curl -s "$SITE/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' \
  | grep -iE 'faq|pricing|compare|vs|docs|support|guide|how-to'
```

## Check for direct-answer patterns on a candidate page

```bash
curl -s "$URL" | grep -ciE '<h[1-6][^>]*>\s*(what|how|why|when|is|can|does)\b'
curl -s "$URL" | grep -oiE '<h[1-6][^>]*>\s*(what|how|why|when|is|can|does)[^<]*'
```

Pages that phrase headings as direct questions are easier for answer engines to extract and cite verbatim.

## Check pricing/comparison clarity (common AI-answer trigger)

```bash
curl -s "$URL" | grep -oiE '\$[0-9,]+(\.[0-9]{2})?'
curl -s "$URL" | grep -ciE '\b(vs\.?|versus|compared to|alternative)\b'
```

Absence of any dollar figure or comparison language on a pricing/comparison-intent page is itself a finding worth recording.

## Check title and meta description length thresholds

The `<title>` and meta description are the exact text AI answer engines and
search-result snippets quote back to a user, so a truncated or missing one
degrades citation quality even when the underlying page content is fine.

```bash
curl -s "$URL" | grep -oE "<title>[^<]*" | sed 's/<title>//'
curl -s "$URL" | grep -oiE '<meta[^>]+name="description"[^>]*content="[^"]*"' \
  | grep -oE 'content="[^"]*"' | sed -e 's/content="//' -e 's/"$//'
```

```bash
curl -s "$URL" | python3 -c "
import re, sys
html = sys.stdin.read()
title = re.search(r'<title>([^<]*)</title>', html, re.IGNORECASE)
desc = re.search(r'<meta[^>]+name=\"description\"[^>]+content=\"([^\"]*)\"', html, re.IGNORECASE)
title_text = title.group(1).strip() if title else ''
desc_text = desc.group(1).strip() if desc else ''
print(f'title ({len(title_text)} chars): {title_text!r}')
print(f'meta description ({len(desc_text)} chars): {desc_text!r}')
"
```

Thresholds, per Ahrefs' documented pixel-truncation research ([AHREFS-TITLE-LENGTH-01],
[AHREFS-META-DESCRIPTION-01] — Google itself truncates by pixel width, not a fixed
character count, but these character ranges are the practical proxy the SEO industry
uses to stay under that pixel width):

- **Title**: keep to roughly 50-60 characters. Titles are commonly readable up to ~60
  characters before Google's pixel-width truncation risk rises sharply; a missing
  `<title>` is a `missing` finding, one over ~60 characters is a `vague` finding
  (present, but likely to be cut off in the exact text an answer engine would quote).
- **Meta description**: keep to roughly 150-160 characters (desktop truncates around
  160; mobile truncates tighter, around 120). A missing meta description is a
  `missing` finding; one that is empty, boilerplate ("Welcome to our website"), or
  over ~160 characters is a `vague` finding.

## Freshness signal check

```bash
curl -s "$URL" | grep -oiE '<meta[^>]+property="article:(published|modified)_time"[^>]*>'
curl -s "$URL" | grep -oiE '(updated|last modified|published)[^<]{0,40}'
```

## Evidence discipline

Record each finding as: URL checked, question it was meant to answer, command run, observed excerpt, and whether the answer is present, vague, missing, or unciteable. Do not claim a content gap without pulling the actual rendered text first.

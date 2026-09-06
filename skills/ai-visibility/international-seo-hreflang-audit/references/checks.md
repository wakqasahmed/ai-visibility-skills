# International SEO & Hreflang Check Commands

Replace `$URL` with the target page URL and `$SITE` with the domain origin.

## 1. Extract HTML `<head>` Hreflang Tags

```bash
# Extract all alternate hreflang link tags from HTML head [GOOGLE-HREFLANG-01]
curl -s "$URL" | grep -oiE '<link[^>]+rel=["'\'']alternate["'\''][^>]+hreflang=["'\''][^"'\'']+["'\''][^>]*>'

# Parse hreflang attribute and href destination
curl -s "$URL" | python3 -c "
import sys, re
from bs4 import BeautifulSoup

html = sys.stdin.read()
soup = BeautifulSoup(html, 'html.parser')
for link in soup.find_all('link', rel=re.compile(r'alternate', re.I)):
    if link.get('hreflang'):
        print(f\"{link.get('hreflang')}: {link.get('href')}\")
"
```

## 1b. Cross-Check Hydrated DOM (Headless Browser)

```bash
# When raw HTML yields 0 hreflang tags on client-rendered SPA/React apps
CHROME=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium \
  || command -v chromium-browser || command -v microsoft-edge || true)
if [ -n "$CHROME" ]; then
  "$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$URL" > /tmp/hydrated_hreflang.html
  grep -oiE '<link[^>]+rel=["'\'']alternate["'\''][^>]+hreflang=["'\''][^"'\'']+["'\''][^>]*>' /tmp/hydrated_hreflang.html
else
  echo "no Chromium-family browser available, hydration cross-check not performed"
fi
```

## 2. Check HTTP Response `Link:` Headers

```bash
# Check for HTTP Link header hreflang annotations (used for non-HTML/PDF or edge routing) [GOOGLE-HREFLANG-01]
curl -sI "$URL" | grep -i "^link:" | grep -i "hreflang"
```

## 3. Verify Return Link Reciprocity (Bidirectional Check)

```bash
# Verify whether target alternate URL points back with reciprocal hreflang [GOOGLE-HREFLANG-01]
TARGET_ALT="https://example.com/es/pagina"
ORIGIN_URL="https://example.com/en/page"

curl -s "$TARGET_ALT" | grep -i "$ORIGIN_URL"
```

## 4. Validate ISO Language and Country Codes

```bash
# Verify code matches ISO 639-1 language and optional ISO 3166-1 alpha-2 region [W3C-ISO-LANG-01]
python3 -c "
import re

valid_iso = re.compile(r'^[a-z]{2}(-[A-Z]{2})?$|^x-default$')
tags = ['en', 'en-US', 'es-ES', 'pt-BR', 'x-default', 'en-UK', 'eng']

for tag in tags:
    is_valid = bool(valid_iso.match(tag))
    # Note: UK is technically not ISO 3166-1 alpha-2 (GB is correct), eng is ISO 639-2
    note = ' (Use GB instead of UK)' if tag == 'en-UK' else ''
    print(f'{tag}: {\"VALID\" if is_valid else \"INVALID\"}{note}')
"
```

## 5. Check Localized Canonical Alignment

```bash
# Ensure localized page has self-referential canonical, not canonical to root [GOOGLE-HREFLANG-01]
curl -s "$URL" | grep -oiE '<link[^>]+rel=["'\'']canonical["'\''][^>]*>'
```

## 6. Inspect Sitemap `xhtml:link` Localized Entries

```bash
# Extract localized sitemap annotations [GOOGLE-HREFLANG-01]
curl -s "$SITE/sitemap.xml" | grep -i "xhtml:link" | head -30
```

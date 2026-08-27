# Paywall & Subscription Content Access Check Commands

Replace `$URL` with the paywalled article URL and `$SITE` with the domain origin.

## 1. Extract and Validate `isAccessibleForFree` JSON-LD Schema

```bash
# Extract JSON-LD paywall schema [GOOGLE-PAYWALL-SCHEMA-01] [SCHEMA-ISACCESSIBLEFORFREE-01]
curl -s "$URL" | python3 -c "
import sys, json, re
from bs4 import BeautifulSoup

html = sys.stdin.read()
soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script', type='application/ld+json')

found_paywall = False
for s in scripts:
    try:
        data = json.loads(s.string)
        items = data if isinstance(data, list) else [data]
        for item in items:
            free = item.get('isAccessibleForFree')
            has_part = item.get('hasPart')
            if free is not None:
                found_paywall = True
                print(f'isAccessibleForFree: {free}')
                print(f'hasPart: {json.dumps(has_part, indent=2)}')
    except Exception:
        continue

if not found_paywall:
    print('No isAccessibleForFree schema markup found.')
"
```

## 2. Verify Lead-In Snippet Renderability in Server HTML

```bash
# Check if public lead paragraph and headline are present in raw HTML payload
curl -s "$URL" | grep -oiE '<p[^>]*>[^<]+' | head -5
```

## 3. Audit AI Training vs. AI Citation Bot Directives in `robots.txt`

```bash
# Check rules for citation bots vs training bots
for bot in GPTBot OAI-SearchBot ClaudeBot Claude-SearchBot PerplexityBot Google-Extended; do
  printf \"%-18s: \" \"$bot\"
  curl -s \"$SITE/robots.txt\" | grep -A 2 -i \"User-agent: $bot\" || echo \"Default / No explicit rule\"
done
```

## 4. Test Paywall CSS Selector Alignment

```bash
# Check if selector declared in hasPart exists in HTML DOM
PAYWALL_SELECTOR=".paywall-content"
curl -s "$URL" | grep -i "$PAYWALL_SELECTOR"
```

# Developer Documentation & API Visibility Check Commands

Replace `$DOCS_URL` with the documentation or API reference URL and `$SITE` with the domain origin.

## 1. Probe Conventional OpenAPI / AsyncAPI / Swagger Schemas

```bash
# Probe standard OpenAPI/Swagger spec paths [OPENAPI-SPEC-01]
for path in "/openapi.json" "/openapi.yaml" "/swagger.json" "/swagger.yaml" "/.well-known/openapi.json" "/api/v1/openapi.json"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$SITE$path")
  echo "$code $SITE$path"
done
```

```bash
# Validate JSON OpenAPI syntax and top-level schema keys [OPENAPI-SPEC-01]
curl -s "$SITE/openapi.json" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    version = data.get('openapi') or data.get('swagger', 'unknown')
    paths_count = len(data.get('paths', {}))
    print(f'Valid OpenAPI spec (version: {version}), contains {paths_count} path definitions.')
except Exception as e:
    print('Failed to parse OpenAPI JSON:', e)
"
```

## 2. Test Server-Side Rendering (SSR) of API Reference Endpoints

```bash
# Check if HTTP methods (GET, POST, PUT, DELETE) and endpoints appear in raw HTML [OPENAPI-SPEC-01]
curl -s "$DOCS_URL" | grep -oiE '(GET|POST|PUT|DELETE|PATCH)\s+/[a-zA-Z0-9_\-\/{}]*' | head -20

# Test for empty client-side SPA shells (e.g. Swagger UI or Redoc without SSR)
curl -s "$DOCS_URL" | grep -oiE '<div[^>]+id=["'\''](swagger-ui|redoc|root|app)["'\''][^>]*>\s*</div>'
```

## 3. Audit Code Block Language Fencing

```bash
# Inspect code blocks for CommonMark language info strings [COMMONMARK-CODE-01]
curl -s "$DOCS_URL" | python3 -c "
import sys, re
from bs4 import BeautifulSoup

soup = BeautifulSoup(sys.stdin.read(), 'html.parser')
blocks = soup.find_all(['pre', 'code'])
tagged = 0
untagged = 0

for b in blocks:
    classes = b.get('class', [])
    lang_classes = [c for c in classes if c.startswith('language-') or c.startswith('lang-')]
    if lang_classes:
        tagged += 1
    else:
        untagged += 1

print(f'Code blocks found: {tagged} language-tagged, {untagged} untagged.')
"
```

## 4. Check for Developer Manifests (`/docs/llms.txt`)

```bash
# Check for curated developer documentation manifest
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/docs/llms.txt"
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/llms-full.txt"
```

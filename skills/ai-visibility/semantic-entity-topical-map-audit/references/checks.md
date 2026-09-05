# Semantic Entity & Topical Map Verification Checks

Read-only inspections for entity grounding and topical structure. Replace `$SITE` with the origin,
`$URL` with the page under test, `$PILLAR_URL` with the pillar page URL, and `$PILLAR_PATH` with
the pillar's path fragment.

Do not pattern-match JSON-LD with `grep -A N '"@type": "Organization"'`. Production sites commonly
emit minified JSON-LD (`"@type":"Organization"`) on a single line, where a literal
colon-plus-space pattern matches nothing and `-A N` spans the whole graph — producing a false
"schema missing" finding. Parse the JSON instead.

---

## 1. Extract and inspect the JSON-LD entity graph

Covers workflow step 1 — `Organization`/`Brand` entity, `@id`, and `sameAs`
`[SCHEMA-ORGANIZATION-01]` `[SCHEMA-SAMEAS-01]` `[GOOGLE-ORG-SCHEMA-01]`.

```bash
curl -s -L "$SITE" | python3 -c "
import sys, json, re

html = sys.stdin.read()
blocks = re.findall(
    r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I
)
if not blocks:
    print('No application/ld+json blocks found in the server HTML.')

def walk(node):
    if isinstance(node, list):
        for item in node:
            yield from walk(item)
    elif isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)

for raw in blocks:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f'UNPARSEABLE JSON-LD block: {exc}')
        continue
    for node in walk(data):
        types = node.get('@type')
        types = types if isinstance(types, list) else [types]
        types = [t for t in types if t]
        if not any(t in ('Organization', 'Brand', 'Corporation', 'LocalBusiness') for t in types):
            continue
        print('@type   :', types)
        print('name    :', node.get('name'))
        print('@id     :', node.get('@id', 'MISSING'))
        same_as = node.get('sameAs')
        print('sameAs  :', json.dumps(same_as) if same_as else 'MISSING')
"
```

Report `@id: MISSING` or `sameAs: MISSING` as findings. Report present `sameAs` targets as
**present**, not verified, until check 2 resolves them.

## 2. Resolve a Wikidata `sameAs` target instead of assuming it

Covers the verification half of workflow step 1. Presence of the property is not evidence that the
target describes this organization; the Wikidata Linked Data interface returns a single item as
JSON at `Special:EntityData/<QID>.json` `[WIKIDATA-DATA-ACCESS-01]`.

```bash
QID="Q00000000"   # substitute the Q-id found in the site's sameAs array
curl -s "https://www.wikidata.org/wiki/Special:EntityData/${QID}.json" | python3 -c "
import sys, json

def pick(terms):
    # An entity's term set can omit 'en' entirely, so fall back rather than
    # reporting a missing English label as 'no such entity'.
    if 'en' in terms:
        return terms['en'].get('value')
    for code in sorted(terms):
        if code.startswith('en'):
            return f\"{terms[code].get('value')} [{code}]\"
    for code in sorted(terms):
        return f\"{terms[code].get('value')} [{code}]\"
    return None

try:
    entities = json.load(sys.stdin).get('entities', {})
except json.JSONDecodeError:
    # An invalid or deleted Q-id returns an HTML error page, not JSON.
    sys.exit('NO SUCH ENTITY - the endpoint did not return JSON for this Q-id')
if not entities:
    print('NO SUCH ENTITY - the Q-id in sameAs does not resolve')
for qid, entity in entities.items():
    print('id         :', qid)
    print('label      :', pick(entity.get('labels', {})))
    print('description:', pick(entity.get('descriptions', {})))
    print('aliases    :', [a['value'] for a in entity.get('aliases', {}).get('en', [])])
"
```

Only report the target as **verified** if the returned label, description, or aliases describe this
organization. Three distinct outcomes, do not collapse them:

- **No entity returned** — the Q-id is wrong or deleted. Treat as a broken identity claim.
- **Entity returned, describes a different subject** — higher severity than a missing `sameAs`: the
  site is actively asserting identity with an unrelated entity.
- **Entity returned but carries no label in any language you can read** — the check is
  *inconclusive*, not a mismatch. Report the target as present-and-unresolved and say why.

## 3. Check canonical `@id` reuse across nested entities

Covers workflow step 2 `[SCHEMA-ORGANIZATION-01]` `[SCHEMA-ARTICLE-01]`.

```bash
curl -s -L "$URL" | python3 -c "
import sys, json, re

def walk(node):
    if isinstance(node, list):
        for item in node:
            yield from walk(item)
    elif isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)

html = sys.stdin.read()
for raw in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        continue
    for node in walk(data):
        for key in ('publisher', 'author', 'brand', 'manufacturer'):
            value = node.get(key)
            if value is None:
                continue
            if isinstance(value, str):
                print(f'{key}: STRING LITERAL ({value!r}) - no @id reference')
            elif isinstance(value, dict):
                print(f'{key}: @id =', value.get('@id', 'MISSING (anonymous nested entity)'))
"
```

A string literal or an anonymous nested object means the page declares a second, disconnected copy
of the entity instead of referencing the canonical one.

## 4. Check author `Person` entity completeness

Covers workflow step 2's author half `[SCHEMA-PERSON-01]` `[GOOGLE-EEAT-AUTHOR-01]`.

```bash
curl -s -L "$URL" | python3 -c "
import sys, json, re

EXPECTED = ('@id', 'jobTitle', 'worksFor', 'alumniOf', 'sameAs')

def walk(node):
    if isinstance(node, list):
        for item in node:
            yield from walk(item)
    elif isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)

html = sys.stdin.read()
found = False
for raw in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        continue
    for node in walk(data):
        types = node.get('@type')
        types = types if isinstance(types, list) else [types]
        if 'Person' not in [t for t in types if t]:
            continue
        found = True
        print('Person:', node.get('name'))
        for prop in EXPECTED:
            print('  ', prop, '=', node.get(prop, 'MISSING'))
        if 'JobTitle' in node:
            print('   WARNING: JobTitle is not a Schema.org property; the property is jobTitle')
if not found:
    print('No Person entity found - authors are likely plain-text bylines only.')
"
```

## 5. Detect orphan subtopic pages, and check subtopic back-links and anchor text to the pillar

Covers workflow step 3 `[AHREFS-TOPIC-CLUSTERS-01]`. A topic cluster requires internal linking
between the pillar page and its subtopic pages; a subtopic with no internal link path from the
pillar is an orphan `[BACKLINKO-ORPHAN-PAGES-01]`. The standard orphan-detection method compares
the linked-to URL set against the sitemap URL set, then the reciprocal check verifies each
subtopic links back to the pillar with descriptive anchor text.

This skill owns the scratch directory created below. Do not reuse it for another skill, and run
both checks in the same shell invocation — `WORK` must stay set for both, since a second,
separately-invoked shell would see it unset and silently resolve `"$WORK"/...` to a bare filename
in the current directory instead of the scratch directory.

```bash
WORK=$(mktemp -d)

# URLs the pillar page actually links to
curl -s -L "$PILLAR_URL" \
  | grep -o -E 'href="[^"#?]+"' | cut -d'"' -f2 | sort -u > "$WORK"/semantic-entity-topical-map-pillar-links.txt

# Candidate subtopic URLs from the sitemap (adjust the path filter to the cluster)
curl -s -L "$SITE/sitemap.xml" \
  | grep -o -E '<loc>[^<]+</loc>' | sed -E 's|</?loc>||g' \
  | grep -E '/blog/|/guides/' | sort -u > "$WORK"/semantic-entity-topical-map-sitemap-urls.txt

# Sitemap URLs with no link from the pillar
comm -13 "$WORK"/semantic-entity-topical-map-pillar-links.txt "$WORK"/semantic-entity-topical-map-sitemap-urls.txt

# Reciprocal check: does each candidate subtopic link back to the pillar, and with what anchor text?
while read -r subtopic; do
  printf '%s -> ' "$subtopic"
  curl -s -L "$subtopic" \
    | grep -o -E "<a[^>]+href=\"[^\"]*${PILLAR_PATH}[^\"]*\"[^>]*>[^<]*" \
    | sed -E 's/.*>//' | head -3 | paste -sd'|' - \
    || echo "NO LINK TO PILLAR"
done < "$WORK"/semantic-entity-topical-map-sitemap-urls.txt
```

Count only what the orphan-detection output lists. Do not extrapolate an orphan count beyond the
URLs actually compared.

Generic anchors (`click here`, `read more`, a bare URL) are a finding in their own right: the link
exists but carries no descriptive signal about the pillar topic.

# Semantic Entity & Topical Map Audit Report: authorityhub.io

## Entity Disambiguation & Knowledge Graph Grounding

- Target: `https://authorityhub.io`
- Entity clarity classification: **FULLY_RECONCILED**
- Detected `@id`: `https://authorityhub.io/#organization` — a stable global URI. `High [Measured]`
- Detected `sameAs` targets, **present** in the markup: a Wikidata item (shown as `Q00000000` in this fixture), a Wikipedia article, a Crunchbase organization page, and a GitHub org page. Presence alone was established by parsing the JSON-LD; it does not establish that the targets describe this organization.
- Wikidata target **verified**: resolving it through the Linked Data interface (`Special:EntityData/<QID>.json` `[WIKIDATA-DATA-ACCESS-01]`) returned an English label and description matching this organization, so the identity claim holds. This is the only `sameAs` target that was resolved; the Wikipedia, Crunchbase, and GitHub URLs remain **present but unresolved**.

## Schema Graph Reconciliation

- The canonical `@id` is referenced — not duplicated — by the `WebSite` entity's `publisher` and by the `author`/`publisher` of every `Article` sampled (5 of 5 sampled article URLs). `High [Measured]`
- Author `Person` entities carry `@id`, `jobTitle`, `worksFor`, and `sameAs` `[SCHEMA-PERSON-01]`; the reader-visible byline matches the marked-up author name, which is what Google's authorship guidance asks for `[GOOGLE-EEAT-AUTHOR-01]`.
- No anonymous nested entity objects and no string-literal `publisher` values were found in the sampled pages.

## Topical Map & Cluster Structure

- Pillar page: `https://authorityhub.io/enterprise-ai-orchestration`.
- Cluster linking is reciprocal: every subtopic URL returned by the sitemap-versus-pillar comparison is linked from the pillar, and each links back to the pillar with descriptive (non-generic) anchor text `[AHREFS-TOPIC-CLUSTERS-01]`.
- Orphan subtopic pages found in the compared URL set: 0 `[BACKLINKO-ORPHAN-PAGES-01]`.

## Recommended Fixes & Schema Graph

No entity-identity or cluster-structure gaps were found in the checks that were run. Two optional follow-ups, both verification rather than markup changes:

1. Resolve the remaining three `sameAs` targets (Wikipedia, Crunchbase, GitHub) so they can be reported as verified rather than present.
2. Re-run the `@id` reconciliation check across a wider article sample; 5 pages were sampled, so consistency across the full archive is unconfirmed.

## Verification Commands

```bash
# 1. sameAs presence, parsed from JSON-LD rather than grepped
curl -s -L "https://authorityhub.io" | python3 -c "
import sys, json, re
for raw in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', sys.stdin.read(), re.S|re.I):
    node = json.loads(raw)
    print(node.get('@id', 'MISSING'), json.dumps(node.get('sameAs', 'MISSING')))
"

# 2. Resolve the declared Wikidata target and confirm it describes this organization
#    (check 2 in references/checks.md; an entity can omit its 'en' label, so fall back
#     rather than reading a missing English label as a mismatch)
QID="Q00000000"   # substitute the Q-id found in the sameAs array above
curl -s "https://www.wikidata.org/wiki/Special:EntityData/${QID}.json" | python3 -c "
import sys, json

def pick(terms):
    if 'en' in terms:
        return terms['en'].get('value')
    for code in sorted(terms):
        return f\"{terms[code].get('value')} [{code}]\"
    return None

entities = json.load(sys.stdin).get('entities', {})
if not entities:
    sys.exit('NO SUCH ENTITY - the Q-id in sameAs does not resolve')
for qid, entity in entities.items():
    print(qid, '|', pick(entity.get('labels', {})), '|', pick(entity.get('descriptions', {})))
"
```

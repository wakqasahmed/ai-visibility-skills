# Semantic Entity & Topical Map Audit Report: techbrand.com

## Entity Disambiguation & Knowledge Graph Grounding

- Target: `https://techbrand.com`
- Entity clarity classification: **AMBIGUOUS**
- Detected `Organization` entity: present (`name`, `url`, `logo`).
- Detected `@id`: `MISSING` — the entity is an anonymous node, so nothing else on the site can reference it. `High [Measured]`
- Detected `sameAs`: `MISSING` — no reference Web page is declared. Schema.org defines `sameAs` as the "URL of a reference Web page that unambiguously indicates the item's identity", naming a Wikipedia page, Wikidata entry, or official website as its examples `[SCHEMA-SAMEAS-01]`. With none present, the markup states a name but makes no machine-readable identity claim beyond it. `High [Measured]`
- No observed AI-engine behaviour is reported here: no engine answer was pasted for this audit, and no engine documents `sameAs` as an input to its entity resolution, so any claim about how a named engine resolves this brand would be unfounded.

## Schema Graph Reconciliation

- Article template emits `"publisher": "TechBrand"` as a string literal rather than an `@id` reference, so each article declares a second, disconnected identity instead of pointing at the canonical one. `High [Measured]`
- `WebSite` entity present but carries no `publisher` property at all. `High [Measured]`
- Author `Person` entities: none — bylines are plain text. `jobTitle`, `worksFor`, and `alumniOf` are therefore all absent `[SCHEMA-PERSON-01]`.

## Topical Map & Cluster Structure

- Pillar page identified: `https://techbrand.com/cloud-infrastructure`.
- Sitemap-versus-pillar-link comparison (check 5) covered 14 `/blog/` URLs; 6 of those 14 have no internal link from the pillar page `[BACKLINKO-ORPHAN-PAGES-01]`. Count is limited to the 14 URLs actually compared — no site-wide extrapolation.

## Recommended Fixes & Schema Graph

1. Give the `Organization` a stable `@id` and add `sameAs` reference pages. **Resolve your organization's real Wikidata Q-id before deploying** — `Q00000000` below is a placeholder, and shipping an arbitrary Q-id asserts identity with an unrelated entity, which is worse than having no `sameAs` at all.

   ```json
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "@id": "https://techbrand.com/#organization",
     "name": "TechBrand",
     "url": "https://techbrand.com",
     "sameAs": [
       "https://www.wikidata.org/wiki/Q00000000",
       "https://www.crunchbase.com/organization/techbrand",
       "https://www.linkedin.com/company/techbrand"
     ]
   }
   ```

   Wikipedia and Wikidata are the reference pages Schema.org itself names `[SCHEMA-SAMEAS-01]`; Crunchbase and LinkedIn are corroborating profiles of the kind Google's `Organization` guidance describes `[GOOGLE-ORG-SCHEMA-01]`.

2. Change the article template's publisher to an `@id` reference: `"publisher": {"@id": "https://techbrand.com/#organization"}` `[SCHEMA-ARTICLE-01]`.
3. Add in-body links from the pillar page to the 6 unlinked `/blog/` URLs listed above, with descriptive anchor text.

## Verification Commands

```bash
# Parse the JSON-LD graph rather than pattern-matching it (minified JSON-LD defeats grep)
curl -s -L "https://techbrand.com" | python3 -c "
import sys, json, re
for raw in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', sys.stdin.read(), re.S|re.I):
    node = json.loads(raw)
    print(node.get('@type'), '| @id:', node.get('@id', 'MISSING'), '| sameAs:', node.get('sameAs', 'MISSING'))
"
```

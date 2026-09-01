# Semantic Entity & Topical Map Audit Report: apex.io

## Entity Disambiguation & Knowledge Graph Grounding

- Target: `https://apex.io`
- Entity clarity classification: **AMBIGUOUS**
- Detected `Organization` entity: present, carrying `name` and `url` only. `High [Measured]`
- Detected `@id`: `MISSING` — the entity is anonymous. `High [Measured]`
- Detected `sameAs`: `MISSING`. `High [Measured]`
- `description` and `alternateName`: `MISSING`, so the markup carries no text distinguishing this "Apex" from any other. `High [Measured]`
- `Medium [Derived]` — inferred risk, not an observation: a common single-word brand name with no `sameAs` reference page and no `@id` gives any consumer of this markup nothing but the string `Apex` to work with. What follows from the evidence is that the site makes no unambiguous identity claim `[SCHEMA-SAMEAS-01]`; how any particular search or answer engine resolves the name was not measured, and no engine documents `sameAs` as an input to its entity resolution. No engine answer was pasted for this audit, so no claim about a named engine's behaviour is made and no competitor or same-name count is asserted.

## Schema Graph Reconciliation

- Because no canonical `@id` exists, the `Article` entities on `/blog/` each emit their own anonymous `Organization` object under `publisher` — five sampled pages produced five disconnected copies `[SCHEMA-ARTICLE-01]`. `High [Measured]`
- No author `Person` entities; bylines are plain text `[SCHEMA-PERSON-01]`.

## Topical Map & Cluster Structure

- No pillar page was identified: the sampled `/product/`, `/solutions/`, and `/blog/` sections each link internally but share no hub page, so there is no pillar-and-cluster structure to measure depth against `[AHREFS-TOPIC-CLUSTERS-01]`.
- Orphan detection was not run, because it compares a sitemap URL set against a pillar's outbound links and there is no pillar to compare against. Reported as not-run rather than as zero orphans.

## Recommended Fixes & Schema Graph

1. Add a stable `@id`, a `description` that states what the company actually does, and `sameAs` reference pages. **Resolve the organization's real Wikidata Q-id first** — `Q00000000` is a placeholder; publishing an arbitrary Q-id asserts identity with an unrelated entity, which is worse than declaring no `sameAs` at all.

   ```json
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "@id": "https://apex.io/#organization",
     "name": "Apex",
     "alternateName": "Apex Developer Tools",
     "description": "Developer tooling for build pipelines and release automation.",
     "url": "https://apex.io",
     "sameAs": [
       "https://www.wikidata.org/wiki/Q00000000",
       "https://www.crunchbase.com/organization/apex",
       "https://www.linkedin.com/company/apex"
     ]
   }
   ```

   If no Wikidata item exists for the organization, omit that line rather than inventing one; the Crunchbase and LinkedIn profiles are corroborating references `[GOOGLE-ORG-SCHEMA-01]`.

2. Replace the per-article anonymous publisher objects with `"publisher": {"@id": "https://apex.io/#organization"}`.
3. Designate a pillar page per product area and link it bidirectionally to its subtopic pages before re-running the cluster check.

## Verification Commands

```bash
# Confirm the Organization entity's identity properties, parsed rather than grepped
curl -s -L "https://apex.io" | python3 -c "
import sys, json, re
for raw in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', sys.stdin.read(), re.S|re.I):
    node = json.loads(raw)
    for prop in ('@type', '@id', 'name', 'alternateName', 'description', 'sameAs'):
        print(prop, '=', node.get(prop, 'MISSING'))
"
```

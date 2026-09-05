# Semantic Entity & Topical Map Audit Report: devtools.co

## Entity Disambiguation & Knowledge Graph Grounding

- Target: `https://devtools.co`
- Entity clarity classification: **PARTIALLY_GROUNDED**
- Detected `@id`: `https://devtools.co/#organization` — stable. `High [Measured]`
- Detected `sameAs`: three targets **present** (GitHub org, X/Twitter, LinkedIn company page); none resolved in this run. No Wikidata or Wikipedia reference page is declared, so the two examples Schema.org names for unambiguous identity are both absent `[SCHEMA-SAMEAS-01]`. The present targets are corroborating profiles of the kind Google's `Organization` guidance describes `[GOOGLE-ORG-SCHEMA-01]`.

## Schema Graph Reconciliation

- `WebSite.publisher` and every sampled `Article.publisher` reference the canonical `@id` rather than duplicating it. `High [Measured]`
- Author `Person` entities present with `@id` and `jobTitle`; `worksFor` and author `sameAs` absent `[SCHEMA-PERSON-01]`.

## Topical Map & Cluster Structure

- Pillar page: `https://devtools.co/microservices-architecture`.
- Sitemap-versus-pillar-link comparison covered 31 `/tutorials/` URLs. 8 of those 31 have no internal link from the pillar page and no inbound internal link from any other page in the compared set — orphans by the standard sitemap-versus-linked-URL comparison `[BACKLINKO-ORPHAN-PAGES-01]`. `High [Measured]`
- The 8 orphaned URLs do link back to the pillar, so the cluster is one-directional: subtopic-to-pillar links exist, pillar-to-subtopic links do not. A topic cluster requires internal linking between all of the pages `[AHREFS-TOPIC-CLUSTERS-01]`.
- The count covers only the 31 URLs compared; it is not an estimate of the whole site.

## Recommended Fixes & Schema Graph

1. Add in-body contextual links from `https://devtools.co/microservices-architecture` to each of the 8 orphaned tutorial URLs, using anchor text naming the subtopic rather than `read more` or a bare URL.
2. Add `worksFor` and `sameAs` to the author `Person` entities so authors resolve to the organization and to a profile page:

   ```json
   {
     "@type": "Person",
     "@id": "https://devtools.co/authors/sam-lee#person",
     "name": "Sam Lee",
     "jobTitle": "Platform Engineer",
     "worksFor": {"@id": "https://devtools.co/#organization"},
     "sameAs": ["https://github.com/example-author"]
   }
   ```

3. Optional: if the organization has a Wikidata item, add it to `sameAs`. Resolve the real Q-id first — `Q00000000` is a placeholder, and an arbitrary Q-id asserts identity with an unrelated entity.

## Verification Commands

```bash
WORK=$(mktemp -d)

# URLs the pillar page actually links to, versus the sitemap's tutorial URLs
curl -s -L "https://devtools.co/microservices-architecture" \
  | grep -o -E 'href="[^"#?]+"' | cut -d'"' -f2 | sort -u > "$WORK"/semantic-entity-topical-map-pillar-links.txt

curl -s -L "https://devtools.co/sitemap.xml" \
  | grep -o -E '<loc>[^<]+</loc>' | sed -E 's|</?loc>||g' \
  | grep -E '/tutorials/' | sort -u > "$WORK"/semantic-entity-topical-map-sitemap-urls.txt

# Sitemap URLs with no link from the pillar
comm -13 "$WORK"/semantic-entity-topical-map-pillar-links.txt "$WORK"/semantic-entity-topical-map-sitemap-urls.txt
```

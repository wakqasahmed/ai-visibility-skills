# Semantic Entity & Topical Map Audit Report: medicalnews.org

## Entity Disambiguation & Knowledge Graph Grounding

- Target: `https://medicalnews.org`
- Entity clarity classification: **PARTIALLY_GROUNDED**
- Detected `@id`: `https://medicalnews.org/#organization` — stable and reused. `High [Measured]`
- Detected `sameAs`: two targets **present** (a Wikipedia article and a LinkedIn company page); neither was resolved in this run, so both are present-not-verified `[SCHEMA-SAMEAS-01]`.
- The organization-level identity is grounded; the gap is at the author level, below.

## Schema Graph Reconciliation

- No `Person` entity exists on any sampled article. Authors and medical reviewers appear only as plain-text bylines, so `jobTitle`, `worksFor`, `alumniOf`, and author `sameAs` are all absent `[SCHEMA-PERSON-01]`. `High [Measured]`
- Note for implementers: the property is `jobTitle`, not `JobTitle` — the capitalized form is not in the Schema.org vocabulary and is silently ignored by consumers.
- `Article` entities reference the canonical organization `@id` correctly for `publisher`, but their `author` value is a bare string `[SCHEMA-ARTICLE-01]`.
- This is reported as a markup-completeness gap. Google's guidance is that it "strongly encourage[s] adding accurate authorship information, such as bylines to content where readers might expect it" `[GOOGLE-EEAT-AUTHOR-01]`; structured `Person` markup is the machine-readable form of that same byline information, not a documented ranking input, so no scoring claim is made here.

## Topical Map & Cluster Structure

- Pillar page: `https://medicalnews.org/cardiology`.
- Sitemap-versus-pillar-link comparison covered 22 `/cardiology/` URLs. Symptom pages and treatment pages are each linked from the pillar, but no sampled symptom page links to its corresponding treatment page, so the cluster is a hub-and-spoke with no lateral links `[AHREFS-TOPIC-CLUSTERS-01]`.
- Orphan subtopic pages in the compared set: 0 `[BACKLINKO-ORPHAN-PAGES-01]`.

## Recommended Fixes & Schema Graph

1. Emit a `Person` entity per author and reviewer, referenced by `@id` from each `Article`:

   ```json
   {
     "@context": "https://schema.org",
     "@type": "Person",
     "@id": "https://medicalnews.org/authors/jane-doe#person",
     "name": "Jane Doe",
     "jobTitle": "Cardiologist",
     "worksFor": {"@id": "https://medicalnews.org/#organization"},
     "alumniOf": "Example University School of Medicine",
     "sameAs": ["https://www.linkedin.com/in/example-author"]
   }
   ```

   Populate `alumniOf` and `sameAs` only from credentials the site can already show on an author page — do not add an affiliation the site does not state.

2. Change each `Article`'s author to `"author": {"@id": "https://medicalnews.org/authors/jane-doe#person"}`.
3. Add lateral links between paired symptom and treatment pages within the cardiology cluster.

## Verification Commands

```bash
# Person entity completeness on a sampled article
curl -s -L "https://medicalnews.org/cardio-guide" | python3 -c "
import sys, json, re
for raw in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', sys.stdin.read(), re.S|re.I):
    node = json.loads(raw)
    author = node.get('author')
    print('author:', json.dumps(author) if author is not None else 'MISSING')
"
```

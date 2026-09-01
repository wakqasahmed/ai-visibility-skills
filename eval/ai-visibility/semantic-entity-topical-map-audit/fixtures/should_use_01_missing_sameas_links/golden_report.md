# Semantic Entity Audit Report: techbrand.com

## Entity Disambiguation & Knowledge Graph Grounding
- Target: `techbrand.com`
- Organization schema status: **PARTIALLY_GROUNDED**
- Detected `sameAs`: None.
- Risk: AI search models confuse `TechBrand` with homonymous legacy brands.

## Schema Graph Reconciliation
- `@id`: Missing stable root entity URI.
- Nested articles use disconnected string literal `"publisher": "TechBrand"` instead of `@id` reference.

## Topical Map & Cluster Structure
- Core Pillar: Cloud Infrastructure.
- Cluster completeness: 14 subtopic articles detected, but 6 lack parent pillar contextual backlinks.

## Recommended Fixes & Schema Graph
1. Add `sameAs` array linking to Wikidata, Wikipedia, and Crunchbase:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://techbrand.com/#organization",
  "name": "TechBrand",
  "url": "https://techbrand.com",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q123456",
    "https://www.crunchbase.com/organization/techbrand"
  ]
}
```
2. Update article templates to reference `"publisher": {"@id": "https://techbrand.com/#organization"}`.

## Verification Commands
```bash
curl -s -L "https://techbrand.com" | grep -A 25 '"@type": "Organization"'
```

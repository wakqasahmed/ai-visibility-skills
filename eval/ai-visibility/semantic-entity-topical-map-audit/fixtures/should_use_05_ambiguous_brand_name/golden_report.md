# Semantic Entity Audit Report: apex.io

## Entity Disambiguation & Knowledge Graph Grounding
- Target: `apex.io`
- Entity Ambiguity Risk: **CRITICAL** (Name "Apex" shares entity tokens with 100+ global brands).
- Missing Wikidata reconciliation causes Perplexity and ChatGPT to conflate developer tools with sports equipment.

## Schema Graph Reconciliation
- Organization schema lacks disambiguating description and `sameAs` entity identifiers.

## Topical Map & Cluster Structure
- Topical hierarchy is fragmented across disconnected landing pages.

## Recommended Fixes & Schema Graph
1. Inject explicit Wikidata Q-identifier and official Crunchbase entity profile in homepage JSON-LD.

## Verification Commands
```bash
curl -s -L "https://apex.io" | grep -A 30 '"@type": "Organization"'
```

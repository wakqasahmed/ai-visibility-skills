# Semantic Entity & Topical Map Verification Checks

Use these read-only inspections to audit entity grounding.

---

## 1. Extract JSON-LD Entity Graph

```bash
curl -s -L "https://example.com" | grep -A 50 'application/ld+json'
```

Look for:
- `"@type": "Organization"`
- `"@id": "https://example.com/#organization"`
- `"sameAs": [ "https://www.wikidata.org/wiki/...", "https://www.crunchbase.com/organization/..." ]`

---

## 2. Check Entity Linking Across Pages

```bash
curl -s -L "https://example.com/blog/article-1" | grep -A 20 '"publisher"'
```

Verify that `"publisher": { "@id": "https://example.com/#organization" }` correctly points to the root entity `@id`.

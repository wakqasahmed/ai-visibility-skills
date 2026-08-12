# Audit findings — sitemap-discovery-audit + llms-txt-generator

### Finding: 40 published blog posts are orphaned from sitemap.xml

- Severity: important
- Evidence: `sitemap-discovery-audit` diff of CMS-published URLs vs `sitemap.xml` entries: 40 URLs published, not listed.
- Source skill: sitemap-discovery-audit
- Reference check: `curl -s "$URL/sitemap.xml" | grep -c "<loc>"`

### Finding: No llms.txt file at site root

- Severity: optional
- Evidence: `curl -s -o /dev/null -w "%{http_code}\n" "$URL/llms.txt"` returns 404.
- Source skill: llms-txt-generator

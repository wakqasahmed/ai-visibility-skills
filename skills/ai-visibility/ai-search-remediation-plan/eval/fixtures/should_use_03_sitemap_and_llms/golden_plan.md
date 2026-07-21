## Add 40 orphaned blog posts to sitemap.xml

- Priority: P1 (important — undiscoverable content)
- Source finding: sitemap-discovery-audit
- Acceptance criteria: `sitemap.xml` lists all 40 previously orphaned blog post URLs.
- Verification:
  ```bash
  curl -s "$URL/sitemap.xml" | grep -c "<loc>"
  # expect: count increases by 40
  ```
- Owner: engineering.

## Publish an llms.txt file at the site root

- Priority: P3 (optional — convenience for AI agents, not blocking)
- Source finding: llms-txt-generator
- Acceptance criteria: `$URL/llms.txt` returns HTTP 200 with a valid llms.txt structure.
- Verification:
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" "$URL/llms.txt"
  # expect: 200 (was: 404)
  ```
- Owner: engineering / content.

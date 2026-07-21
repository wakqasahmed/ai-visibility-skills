# AI Visibility Audit — docs.paperlantern.example

Overall: partially ready

- [IMPORTANT] sitemap.xml declared in robots.txt returns HTTP 404
  evidence: curl -s -o /dev/null -w "%{http_code}\n" https://docs.paperlantern.example/sitemap.xml — "404"; over 200 docs pages have no other discoverable index
  delegate for deep dive: sitemap-discovery-audit

This audit reports observed evidence only. It does not claim inclusion or ranking on any AI platform.

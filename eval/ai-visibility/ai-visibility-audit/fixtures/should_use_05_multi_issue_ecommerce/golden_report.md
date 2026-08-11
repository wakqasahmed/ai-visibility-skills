# AI Visibility Audit — cascadekettles.example

Overall: blocked

- [CRITICAL] robots.txt blocks CCBot from the entire site
  evidence: robots.txt — "Disallow: /" under "User-agent: CCBot"
  delegate for deep dive: robots-ai-crawler-audit
- [IMPORTANT] No Product JSON-LD structured data on product pages
  evidence: /products/copper-kettle — no <script type="application/ld+json"> block found
  delegate for deep dive: schema-markup-audit
- [OPTIONAL] Return policy FAQ answer has no link or detail to cite
  evidence: /faq — "What's your return policy?" answered only with "See our policy page." and no link
  delegate for deep dive: citation-readiness-audit

This audit reports observed evidence only. It does not claim inclusion or ranking on any AI platform.

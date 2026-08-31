# AI Visibility Audit — harborline.example

Overall: partially ready

- [IMPORTANT] Pricing-page JSON-LD is present in the hydrated DOM but absent from the initial server response
  evidence: /pricing — raw `curl` matched 0 <script ... application/ld+json> blocks (body is 190 self.__next_f.push(...) RSC chunks); `chrome --headless=new --dump-dom` on the same URL returned 2 well-formed blocks (Organization, BreadcrumbList). The entities exist, so this is a Pillar 2 delivery gap (rubric 2.8, -15), not a Pillar 3 absence — but GPTBot, ClaudeBot and PerplexityBot do not execute JavaScript and therefore read a page with no structured data.
  delegate for deep dive: schema-markup-audit

Title, meta description and canonical are all present in the raw homepage response and need no
fix: they carry a `data-react-helmet="true"` attribute ahead of the attribute being matched, so
they are only invisible to an adjacent-token pattern such as `grep '<meta name="description"'`,
not to a crawler. Verified with `curl -s https://harborline.example | grep -oiE '<meta[^>]+name="description"[^>]*>'`,
which returns the tag.

This audit reports observed evidence only. It does not claim inclusion or ranking on any AI platform.

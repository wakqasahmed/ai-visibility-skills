## Finding: What does Acme Plan cost?

- URL: https://acmeplan.example/pricing
- Question: What does the Acme Plan subscription cost?
- Command: `curl -s https://acmeplan.example/pricing | python3 -c "..."` (rendered-text extraction)
- Observed: no output — server-rendered HTML is a single `<div id="app"></div>` root with no pricing text; the pricing table is injected client-side by JS after load
- Status: missing
- Severity: critical
- Recommendation: server-render the pricing table (or provide a static fallback) so the plan names, prices, and billing cadence are present in the raw HTML AI crawlers fetch. Client-side-only rendering means answer engines see nothing to cite for this page.

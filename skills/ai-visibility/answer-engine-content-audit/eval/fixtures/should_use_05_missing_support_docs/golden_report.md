## Finding: How do I export my data from Acme Plan?

- URL: https://acmeplan.example/docs
- Question: How do I export my data from Acme Plan?
- Command: `curl -s https://acmeplan.example/docs | grep -ci "export"`
- Observed: 0 — no mention of data export anywhere in the docs section headings (Getting Started, Integrations, API Reference) or body
- Status: missing
- Severity: important
- Recommendation: add a "How do I export my data?" doc page or section covering export formats and steps, since data-portability questions are common before a purchase or churn decision.

## Finding: Can I get a refund if I cancel Acme Plan mid-cycle?

- URL: https://acmeplan.example/refund-policy
- Question: Can I get a refund if I cancel Acme Plan mid-cycle, and under what conditions?
- Command: `curl -s https://acmeplan.example/refund-policy | python3 -c "..."` (rendered-text extraction)
- Observed: "Refunds are handled on a case-by-case basis. Contact support for details." — no stated conditions, timeframe, or proration rule
- Status: vague
- Severity: important
- Recommendation: state the actual refund conditions (e.g. prorated within N days, no refund after usage threshold) so assistants can answer the mid-cycle-cancellation question directly instead of deflecting to "contact support."

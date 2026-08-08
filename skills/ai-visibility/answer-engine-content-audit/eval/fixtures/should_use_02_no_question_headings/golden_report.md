## Finding: Why is Acme Plan not syncing with Google Calendar?

- URL: https://acmeplan.example/support/sync-errors
- Question: Why is Acme Plan not syncing with Google Calendar, and how do I fix it?
- Command: `curl -s https://acmeplan.example/support/sync-errors | grep -ciE '<h[1-6][^>]*>\s*(what|how|why|when|is|can|does)\b'`
- Observed: 0 — headings are labels ("Common Issues", "Calendar Integration", "Contact Support"), none phrased as the actual question a user or AI assistant would ask
- Status: unciteable
- Severity: important
- Recommendation: rephrase the "Calendar Integration" section as a direct-answer heading such as "Why isn't Acme Plan syncing with Google Calendar?" followed by the specific causes and fixes, so answer engines can extract and cite it verbatim.

## Finding: What features does CloudApp support?

- URL: https://cloudapp.example/features
- Question: What features does CloudApp support?
- Command: `curl -s https://cloudapp.example/features | grep -oE "<h1[^>]*>[^<]+"`
- Observed: no output — server-delivered HTML is an empty `<div id="root"></div>` shell; feature headings and body copy exist only after client-side hydration
- Status: missing
- Severity: critical
- Recommendation: Server-side render the features page (or provide static HTML fallback) so that headings and feature descriptions are present in the initial HTTP payload. Purely client-side rendered content is invisible to non-JS executing AI search crawlers.

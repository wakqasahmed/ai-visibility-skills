## Finding: What features does CloudApp support?

- URL: https://cloudapp.example/features
- Question: What features does CloudApp support?
- Command: raw pass `curl -s https://cloudapp.example/features | grep -oE "<h1[^>]*>[^<]+"` → no output; hydrated pass `chromium --headless=new --disable-gpu --dump-dom https://cloudapp.example/features | grep -oE "<h1[^>]*>[^<]+"` → `<h1 class="hero-title">CloudApp Features</h1>`
- Observed: raw HTML is an empty `<div id="root"></div>` shell with no output from the raw pass, but the hydrated DOM pass finds the feature headings and body copy — present in the rendered DOM but absent from the initial server response, invisible to non-JS-executing crawlers (GPTBot, ClaudeBot, PerplexityBot)
- Status: missing
- Severity: important
- Recommendation: Server-side render the features page (or provide a static HTML fallback) so that headings and feature descriptions are present in the initial HTTP payload. The content is correct and complete once rendered — the gap is delivery, not authoring — but purely client-side rendered content is still invisible to non-JS executing AI search crawlers.

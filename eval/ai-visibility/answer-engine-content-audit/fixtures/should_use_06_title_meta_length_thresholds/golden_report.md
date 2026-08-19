## Finding: Will the Summit 3 tent's title display in full in AI-generated snippets?

- URL: https://denali-outfitters.example/products/summit-3-tent
- Question: Will the page title display in full within Google/AI-generated snippet previews, or will it truncate mid-sentence?
- Command: `curl -s https://denali-outfitters.example/products/summit-3-tent | grep -oE "<title>[^<]*"`
- Observed: `118` characters — `Summit 3 Ultralight 3-Person Backpacking Tent for Extreme Weather Camping and Mountaineering Trips | Denali Outfitters` — well over the ~50-60 character range Ahrefs documents as the practical threshold before Google's pixel-width truncation risk rises sharply (`AHREFS-TITLE-LENGTH-01`)
- Status: vague
- Severity: important
- Recommendation: shorten the title to roughly 50-60 characters, front-loading the product name and its distinguishing feature (e.g. "Summit 3 Ultralight 3-Person Backpacking Tent | Denali Outfitters"), so the full title is what AI answer engines quote back instead of a mid-word cutoff.

## Finding: Does the Summit 3 tent page have a citeable meta description?

- URL: https://denali-outfitters.example/products/summit-3-tent
- Question: Does the meta description give AI systems and search snippets a complete, quotable summary of the page?
- Command: `curl -s https://denali-outfitters.example/products/summit-3-tent | grep -oiE '<meta[^>]+name="description"[^>]*>'`
- Observed: no output — no `<meta name="description">` tag is present anywhere in the raw HTML, matching Perplexity's "no description available" answer
- Status: missing
- Severity: critical
- Recommendation: add a meta description of roughly 150-160 characters (Ahrefs documents Google's desktop truncation point at ~920px / ~160 characters, tighter on mobile — `AHREFS-META-DESCRIPTION-01`) summarizing the tent's key selling points, so answer engines have a first-party summary to quote instead of guessing or reporting none found.

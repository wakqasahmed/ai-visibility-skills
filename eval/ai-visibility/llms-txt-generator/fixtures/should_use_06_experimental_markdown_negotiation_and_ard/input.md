Draft an `llms.txt` for `https://developer-hub.io/` from the observed public pages below, and also probe experimental discovery channels (Markdown content-negotiation and auth.md/ard.json manifests).

Observed evidence:
- Existing `https://developer-hub.io/llms.txt`: HTTP 404
- Title: "DeveloperHub | Fast API Integration Tools"
- Meta description: "DeveloperHub gives teams instant APIs and developer tooling."
- Sitemap URLs (all verified HTTP 200):
  - `https://developer-hub.io/` (Homepage)
  - `https://developer-hub.io/docs` (Documentation index)
  - `https://developer-hub.io/api` (API Reference)
  - `https://developer-hub.io/pricing` (Pricing & Usage)
- Experimental check `Accept: text/markdown`:
  - `curl -s -i -H "Accept: text/markdown" https://developer-hub.io/docs` returned `content-type: text/markdown; charset=utf-8` and raw markdown body.
- Experimental check `auth.md` & `ard.json`:
  - `curl -s -o /dev/null -w "%{http_code}\n" https://developer-hub.io/auth.md` returned `404`
  - `curl -s -o /dev/null -w "%{http_code}\n" https://developer-hub.io/.well-known/ard.json` returned `404`

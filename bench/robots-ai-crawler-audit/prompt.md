# robots-ai-crawler-audit — bench prompt

**Source**: real audit run against `missioncontrolhq.ai` on 2026-08-18, using this skill's `references/checks.md` methodology (robots.txt fetch, per-bot live fetch, page-level directive checks) plus a manual sitemap/llms.txt content-type and body check.

## Prompt

Given the raw HTTP evidence below (robots.txt contents, per-bot-UA status codes, response headers, and homepage HTML), audit whether AI answer-engine crawlers (GPTBot, ClaudeBot, PerplexityBot) can both reach and meaningfully read missioncontrolhq.ai. Report each finding as: what was checked, the observed evidence, and whether it helps or hurts AI-crawler visibility. Do not infer a block or a gap without evidence in the data provided — and do not report a 200 status code alone as proof a file exists; check the content-type and body too.

## Input 1

```
robots.txt:
# App routes are auth-gated SPA shells with no crawlable content.
# /share/:token is deliberately NOT disallowed: share pages carry a rendered
# noindex (RouteSeo), and Google must be able to crawl a page to see it.
User-agent: *
Disallow: /dashboard
Disallow: /setup
Disallow: /admin
Disallow: /billing
Disallow: /integrations
Disallow: /email-domains
Disallow: /sprites-signup
Disallow: /onboarding
Disallow: /old/
Disallow: /v1/
Disallow: /i/
Disallow: /agent/

Sitemap: https://missioncontrolhq.ai/sitemap.xml
Sitemap: https://missioncontrolhq.ai/resources/sitemap.xml
```

### Correct output 1

No AI bot (GPTBot, ClaudeBot, PerplexityBot, etc.) has its own User-agent stanza — every one falls under the general `*` wildcard, which only disallows auth-gated app-shell paths, not public content. Two sitemaps are declared. Verdict: helps visibility — access is open.

## Input 2

```
Per-bot live fetch: GPTBot 200, ClaudeBot 200, PerplexityBot 200, Google-Extended 200, CCBot 200, Amazonbot 200, Googlebot 200
```

### Correct output 2

All 7 tested crawler UAs got genuine HTTP 200s with real page content in the body (confirmed separately, not a captcha/soft-block). Verdict: helps visibility — no edge/WAF block.

## Input 3

```
Homepage <head> meta tags present: charset, viewport, theme-color, og:title, og:type, og:site_name, og:url, og:image (+dims), twitter:card, twitter:title, twitter:image. NOT present: meta name="description", og:description.
```

### Correct output 3

Open Graph and Twitter Card tags are complete, but there is no meta description and no og:description at all. Verdict: hurts visibility — AI/search snippets have no summary to draw from and must fall back to body text.

## Input 4

```
Homepage rendered-text (script/style stripped, tags stripped): 291 characters, mostly a build-tooling HTML comment plus the <title> tag.
```

### Correct output 4

The server-delivered text content is ~291 characters, almost entirely a developer comment and the title — not real page copy. Verdict: hurts visibility for non-JS crawlers — actual content is client-rendered and invisible without executing JavaScript.

## Input 5

```
Static JSON-LD present in initial HTML (no JS execution needed): Organization + WebSite @graph, includes founder name and social links.
```

### Correct output 5

A schema.org Organization + WebSite JSON-LD block is present in the raw HTML, readable without JS, including founder name and social links. Verdict: helps visibility, but only for entity-identity questions (who is this company) — it does not substitute for missing body/product content.

## Input 6

```
sitemap.xml: HTTP 200, content-type application/xml, real XML sitemap body.
```

### Correct output 6

sitemap.xml is genuine — correct content-type, real URLs in the body. Verdict: helps visibility — a real discovery path exists.

## Input 7

```
llms.txt: HTTP 200, content-type text/html, body is the SPA's index.html shell.
```

### Correct output 7

llms.txt returns 200, but content-type is text/html (should be text/plain) and the body is the site's app shell, not real llms.txt content — a false positive a status-code-only check would miss. Verdict: hurts visibility (or neutral-at-best) — no real llms.txt exists.

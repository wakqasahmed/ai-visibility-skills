# Prompt Guide — getting a good run out of this pack

This is not a prompt-engineering tutorial. It is about this pack specifically: what to type, what to hand over before the run starts, and what this pack currently gets wrong that you have to double-check by hand.

Related, and deliberately not repeated here: [`RUNNING_AN_AUDIT.md`](RUNNING_AN_AUDIT.md) covers installing the pack and running it from your own terminal, and [`EXAMPLE_PROMPTS.md`](EXAMPLE_PROMPTS.md) is a per-skill catalogue of illustrative prompts with the report shape each one produces. Read those for *what to run*; read this for *how to ask*.

Last verified against the pack on 2026-08-31.

## Quick start

The pack has fourteen skills, but you almost never pick one. `ai-visibility-audit` is the orchestrator: it classifies the site, runs its own discovery and machine-readability pass, and delegates everything deeper to the specialist skill that owns it. Name it and let it fan out.

```
Use the ai-visibility-audit skill on https://example.com. Show the command output behind
each finding, and give me the prioritized action plan at the end.
```

That is enough for a real run. Everything below is about making it better.

Reach past the orchestrator only when you already know which dimension you care about — `robots-ai-crawler-audit` for a crawler-access question, `llms-txt-generator` to draft a file, `ai-search-remediation-plan` to turn findings you already have into tickets.

## Giving useful context

Each item below changes what the pack does, not just how the report reads. That is the test for whether something belongs in your prompt.

| Supply this | Why it changes the run |
|---|---|
| **The full URL, with scheme** | The pack classifies business model from the site itself, and that classification gates which specialist skills fire at all. A bare domain name means the first thing the agent does is guess. |
| **What the site actually is**, if it is not obvious from the homepage | The Capability Gating Matrix in `ai-visibility-audit` keys on ecommerce, multilingual, developer-platform, and paywalled signals. Say "ecommerce, 400 SKUs" or "docs site with an OpenAPI spec" and the matching specialist runs instead of being marked `N/A`. |
| **Scope: one page, a section, or the whole site** | Several skills sample rather than crawl — `ecommerce-technical-seo-audit` samples 3-5 pages by design. If you need a specific template audited, name that URL. |
| **Any private data you can supply** — Search Console exports, analytics, server logs | A guardrail in the pack says to prefer public crawlable evidence *unless* you provide private data. Supplying it moves findings from `[Derived]` to `[Measured]`. Not supplying it is fine; just know which half of the report you are getting. |
| **Who reads the output** | An executive dashboard, a developer ticket list, and a client PDF are three different deliverables from the same findings. |
| **Whether you want the PDF** | Rendering runs `scripts/render-audit-pdf.py` over the Markdown report. Ask for it in the same prompt rather than as an afterthought. |
| **What you already tried** | Stops the agent re-reporting a fix you shipped last week as an open finding. |

One thing you do **not** need to supply: any special syntax. Plain language naming the skill is the invocation.

## Structuring a complex or multi-phase request

For anything past a single audit — audit, then remediate, then export — give the request its own structure instead of one long sentence. Markdown headers and XML tags work equally well here; what matters is that instructions, context, and the ask are visibly separate, and that you stay consistent inside one prompt.

```
# Instructions
1. Run ai-visibility-audit against https://example.com.
2. Hand the ranked findings to ai-search-remediation-plan and produce P0-P3 tickets.
3. Format with the standardized audit report template and render a PDF into output/.

# Context
Ecommerce storefront, ~400 SKUs, Next.js, no Search Console access available.
Previous audit six months ago fixed robots.txt; assume that part is clean and re-verify cheaply.

# Constraints
- Cite the exact command and observed output for every finding. A finding with no
  evidence is worse than no finding, because it looks authoritative.
- Mark experimental protocol findings clearly; they must not affect the core score.

# Output format
Executive dashboard first, then the P0-P3 plan, then the technical appendix.
```

Two placement rules worth following. Put bulk material — a long list of URLs, a pasted robots.txt, a previous report — near the top, above the actual ask, and keep the ask last. And attach the reason to each constraint rather than just stating it; "cite the command because a finding with no evidence looks authoritative" generalizes to cases you did not anticipate, where a bare "cite commands" does not.

## Good vs. less-effective prompt examples

**Pair 1 — name the skill and the scope**

Less effective:

```
check if my site is AI friendly
```

More effective:

```
Use the ai-visibility-audit skill on https://example.com. It's a docs site with an
OpenAPI spec at /openapi.json. Focus on Pillars 1-3; skip trust and authority for now.
```

The second version gets the developer-platform gate to fire (so `docs-api-visibility-audit` actually runs) and bounds the work. The first version produces something, but the site type is a guess and the scope is whatever the agent decides.

**Pair 2 — say what evidence you will accept**

Less effective:

```
audit example.com and tell me what's broken
```

More effective:

```
Audit https://example.com with ai-visibility-audit. For every finding show the exact
command and its output — I need to hand this to a developer who will re-run it. Where
you're inferring rather than observing, label it [Derived] and say what would confirm it.
```

The pack already separates `[Measured]` from `[Derived]`; asking for it explicitly, and saying *why* (someone else re-runs these), reliably gets the appendix filled in rather than summarized away.

**Pair 3 — chain the phases instead of asking twice**

Less effective:

```
run an audit
```
…then, a dozen turns later:
```
now make tickets
```

More effective:

```
Run ai-visibility-audit on https://example.com, then pass the ranked findings to
ai-search-remediation-plan and give me P0-P3 tickets with verification commands.
```

Chaining in one request keeps the findings and their evidence in the same context as the tickets. Asking later often gets tickets rebuilt from the summary, with the command output lost.

## Known limitations to mention explicitly

Real, currently-open gaps. Each one is something to verify by hand if it matters for your site. Status as of 2026-08-31 — re-check the linked issues before relying on this.

- **JavaScript-hydrated content can produce false negatives.** ([#102](https://github.com/wakqasahmed/ai-visibility-skills/issues/102), fix open and unmerged in [PR #104](https://github.com/wakqasahmed/ai-visibility-skills/pull/104).) Reading raw HTML only, the pack missed React-Helmet head tags and Next.js RSC-streamed JSON-LD, reporting "zero structured data" for a page carrying four valid blocks. PR #104 adds a hydrated-DOM second pass, but scoped to **title, meta description, canonical, and JSON-LD only** — its own self-assessment states that other raw-HTML checks in the pack (hreflang, `h1`/body extraction, image `src`) still have the same blind spot and were left untouched. Until it merges, none of it is on `main`.

  What to do: if your site is client-rendered, say so in your prompt and ask for a rendered-DOM check explicitly. Treat any "absent" finding for head metadata, hreflang, headings, or images as unresolved rather than confirmed until you have viewed the hydrated page yourself.

- **Sitemap discovery guesses filenames.** ([#103](https://github.com/wakqasahmed/ai-visibility-skills/issues/103), fix open and unmerged in [PR #105](https://github.com/wakqasahmed/ai-visibility-skills/pull/105).) `sitemap-discovery-audit` probes `/sitemap.xml` and `/sitemap_index.xml`. A `gatsby-plugin-sitemap` site publishing `/sitemap-index.xml` — hyphenated — was reported as having no sitemap at all. PR #105 reorders discovery to follow what the site declares (`robots.txt` directives, then `<link rel="sitemap">`, then defaults) and adds host-consistency checking, but is not merged.

  What to do: if a run says you have no sitemap, check your generator's actual output path before believing it.

- **A `200` is not proof a file exists.** Anti-bot challenge pages and SPA fallback shells both return `200` for any path. This one is documented and guarded in `RUNNING_AN_AUDIT.md` §5 rather than being a bug — ask for the response headers and the first lines of the body, not the status code.

- **Some skills sample; they do not crawl.** `ecommerce-technical-seo-audit` spot-checks 3-5 pages. `commerce-protocol-discovery` reports what agentic-commerce surfaces exist and does not score readiness or remediate. Neither is a full-catalog guarantee.

- **Experimental protocol findings are not requirements.** `llms.txt`, ARD, DNS-AID, and Content Signals are draft conventions, labeled `[EXPERIMENTAL]`, and by design never reduce the core 100-point score. If a report or a vendor tells you a missing `llms.txt` is hurting your AI visibility today, that claim is not supported here.

- **The example prompts are illustrative, not test runs.** `EXAMPLE_PROMPTS.md` says so at the top: none have been executed against a live site and recorded.

## Where to go deeper

- [`skills/ai-visibility/ai-visibility-audit/SKILL.md`](../skills/ai-visibility/ai-visibility-audit/SKILL.md) — the orchestrator: 6-pillar model, capability gating matrix, evidence tiers, delegation table.
- [`README.md`](../README.md) — install methods, the full skill table, and the design principle behind the delegation structure.
- [`RUNNING_AN_AUDIT.md`](RUNNING_AN_AUDIT.md) — prerequisites, install, verification, and the two most common false positives.
- [`EXAMPLE_PROMPTS.md`](EXAMPLE_PROMPTS.md) — fifteen worked prompts, one per scenario, with the report shape each promises.
- [`AUDIT_REPORTING_GUIDE.md`](AUDIT_REPORTING_GUIDE.md) and [`SCORING_RUBRIC.md`](SCORING_RUBRIC.md) — deliverable formatting and how a score is derived rather than asserted.

---

Generated with the `write-prompt-guide` skill from [`wakqasahmed/ai-engineering-workflow-skills`](https://github.com/wakqasahmed/ai-engineering-workflow-skills/blob/main/skills/engineering/write-prompt-guide/SKILL.md), whose methodology is cited against the official prompting documentation of Anthropic, OpenAI, Google, and BytePlus.

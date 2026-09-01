# Example prompts

**These are illustrative usage examples, not verified test runs.** Nobody has executed
these prompts against a live website and recorded the real output yet — this file shows
what you'd type and what kind of report structure the invoked skill's own `SKILL.md`
promises, grounded in each skill's `## Output` section. It does not claim any of these
runs actually happened. If you run one of these for real and want to contribute the actual
output, open a PR that replaces the relevant "expected output shape" block with the real
result and a link to the evidence (e.g. a saved run log or PR that used it).

This distinction matters because this pack's own [shared guardrails](../skills/ai-visibility/references/guardrails.md)
say: don't present an inference as an observed result. Labeling these as tested would
violate that principle.

---

## Example 1 — general AI visibility check

**Skill invoked:** [`ai-visibility-audit`](../skills/ai-visibility/ai-visibility-audit/SKILL.md)

**Prompt:**

> "Can ChatGPT, Perplexity, and Google AI Overviews find and cite our site,
> `https://example-store.com`? Run an AI visibility audit and tell me what's blocking us."

**Expected output shape** (per the skill's `## Output` section):

- Overall score — ready, partially ready, or blocked
- Top 5 blockers
- Evidence with URLs (observed page evidence, not inferred)
- Quick wins
- Implementation tickets or next actions

---

## Example 2 — crawler access review

**Skill invoked:** [`robots-ai-crawler-audit`](../skills/ai-visibility/robots-ai-crawler-audit/SKILL.md)

**Prompt:**

> "Check `robots.txt` and any meta-robots/header rules on `https://example-store.com` —
> are we accidentally blocking GPTBot, ClaudeBot, or PerplexityBot from our product and
> docs pages?"

**Expected output shape:**

- Current crawler policy summary
- Blocked high-value paths
- AI crawler implications
- Recommended `robots.txt` changes
- Verification commands

---

## Example 3 — llms.txt drafting

**Skill invoked:** [`llms-txt-generator`](../skills/ai-visibility/llms-txt-generator/SKILL.md)

**Prompt:**

> "Draft an `llms.txt` for `https://example-store.com` using our sitemap, product pages,
> and support docs, so AI agents know which pages matter most."

**Expected output shape:**

- Proposed `llms.txt` content
- Placement path (`/llms.txt`)
- Source URLs used
- Missing recommended URLs or pages
- Verification steps

---

## Example 4 — audit findings into a remediation plan

**Skills invoked:** [`schema-markup-audit`](../skills/ai-visibility/schema-markup-audit/SKILL.md)
then [`ai-search-remediation-plan`](../skills/ai-visibility/ai-search-remediation-plan/SKILL.md)

**Prompt:**

> "Audit our schema.org JSON-LD on `https://example-store.com/products/*` for AI search
> and rich results, then turn whatever you find into a prioritized implementation
> checklist I can hand to engineering."

**Expected output shape:**

From `schema-markup-audit`:
- Existing schema types found
- Missing or weak schema
- Mismatches with visible content
- Recommended JSON-LD changes
- Verification tools or commands

Fed into `ai-search-remediation-plan`, which turns those findings into:
- Priority roadmap
- Issue-sized tasks
- Acceptance criteria
- Verification commands or manual checks
- Owner decisions and blockers

---

## Example 5 — sitemap and crawl discovery audit

**Skill invoked:** [`sitemap-discovery-audit`](../skills/ai-visibility/sitemap-discovery-audit/SKILL.md)

**Prompt:**

> "Audit our sitemaps and discovery paths on `https://example-store.com` — are all
> high-value pages included, and are there broken links, redirect loops, or non-canonical
> URLs in the sitemap or on-page links?"

**Expected output shape:**

- Sitemap paths found
- Coverage gaps
- Broken or blocked URLs
- Canonical and redirect issues
- Priority fixes

---

## Example 6 — answer engine content gap audit

**Skill invoked:** [`answer-engine-content-audit`](../skills/ai-visibility/answer-engine-content-audit/SKILL.md)

**Prompt:**

> "Audit `https://example-store.com` for content gaps that prevent AI answer engines
> (Perplexity, ChatGPT Search, Google AI Overviews) from answering customer questions about
> our pricing, product comparisons, and support policies."

**Expected output shape:**

- Question-to-URL map
- Missing high-intent answers
- Weak or vague answers
- Title/meta description length findings (see `references/checks.md`)
- Recommended page updates
- New page ideas with priority

---

## Example 7 — citation readiness and trust audit

**Skill invoked:** [`citation-readiness-audit`](../skills/ai-visibility/citation-readiness-audit/SKILL.md)

**Prompt:**

> "Audit `https://example-store.com` to see if our product claims, pricing, and company
> information are structured and sourced well enough for AI engines to cite them reliably."

**Expected output shape:**

- Claims and canonical URLs
- Citation blockers
- Trust and freshness gaps
- Recommended page fixes
- Claims to remove or substantiate

---

## Example 8 — image discoverability and fetchability audit

**Skill invoked:** [`image-audit`](../skills/ai-visibility/image-audit/SKILL.md)

**Prompt:**

> "Check whether the product and hero images on `https://example-store.com/products/wireless-headphones`
> are visible to AI crawlers and multimodal agents — check alt text quality, image sitemap coverage,
> ImageObject schema, and whether lazy loading requires JavaScript without a noscript fallback."

**Expected output shape:**

- Alt text coverage and quality summary (key pages sampled, missing/weak count)
- Image sitemap coverage summary (declared vs. found on page)
- `ImageObject` schema presence and completeness
- Fetchability findings (JS-only lazy-load without fallback, auth/geo-blocked images)
- Recommended fixes
- Verification commands

---

## Example 9 — ecommerce catalog technical SEO spot-check

**Skill invoked:** [`ecommerce-technical-seo-audit`](../skills/ai-visibility/ecommerce-technical-seo-audit/SKILL.md)

**Prompt:**

> "Spot-check 3-5 category and product pages on `https://example-store.com` for ecommerce
> technical-SEO issues: thin category descriptions, faceted-navigation URL duplicates without
> canonicals, orphan products, and how discontinued items are handled."

**Expected output shape:**

- Sample scope (exact pages/URLs checked, and that this is a sample, not the full catalog)
- Thin category/collection page findings (word count, duplication)
- Faceted-navigation duplicate URL findings
- Orphan page findings
- Discontinued-product handling findings
- Recommended fixes
- Verification commands

---

## Example 10 — standalone remediation plan generation

**Skill invoked:** [`ai-search-remediation-plan`](../skills/ai-visibility/ai-search-remediation-plan/SKILL.md)

**Prompt:**

> "Here are the raw findings from our AI visibility and crawler audit on `https://example-store.com`.
> Turn them into prioritized, independently verifiable engineering tickets with exact acceptance
> criteria and re-runnable commands."

**Expected output shape:**

- Priority roadmap
- Issue-sized tasks
- Acceptance criteria
- Verification commands or manual checks
- Owner decisions and blockers

---

## Example 11 — full audit including experimental emerging agent discovery signals

**Skills invoked:** [`ai-visibility-audit`](../skills/ai-visibility/ai-visibility-audit/SKILL.md)

**Prompt:**

> "Audit `https://example-store.com` for AI search visibility, and also probe emerging draft
> agent discovery standards (DNS-AID, Content Signals in robots.txt, Web Bot Auth, Markdown
> content negotiation, and Auth.md/ARD manifests). Clearly mark any draft protocol findings."

**Expected output shape:**

- Overall score: ready, partially ready, or blocked
- Top 5 blockers
- Evidence with URLs
- Quick wins
- **`## [EXPERIMENTAL] Emerging Agent Signals (Draft Standards)`**:
  - Content Signals status (`Content-Signal:` in `robots.txt`)
  - Web Bot Auth status (`/.well-known/http-message-signatures-directory` / HTTP signatures)
  - DNS-AID SVCB/HTTPS records (`example-store.com` HTTPS/SVCB records)
  - Markdown content negotiation (`Accept: text/markdown` response)
  - Agential Resource Discovery manifests (`/auth.md`, `/.well-known/ard.json`)
  - Explicit disclaimer: *"Note: These checks evaluate emerging draft standards. Absence of these signals does not block search indexing or established AI crawler access."*
- Implementation tickets or next actions

---

## Example 12 — full audit with automated executive PDF and HTML deliverable generation

**Skills invoked:** [`ai-visibility-audit`](../skills/ai-visibility/ai-visibility-audit/SKILL.md)

**Prompt:**

> "Run a full AI visibility audit against `https://example-saas.com/`, compile the report following
> the standardized template, and generate an executive PDF and HTML report in the `output/` directory."

**Workflow executed:**

1. The agent invokes `ai-visibility-audit` and runs discoverability, crawler access, structured data, on-page headings, and experimental signal probes.
2. The agent formats the findings into `output/example-saas-com-ai-visibility-audit.md` following [`docs/templates/AUDIT_REPORT_TEMPLATE.md`](templates/AUDIT_REPORT_TEMPLATE.md).
3. The agent executes `python scripts/render-audit-pdf.py output/example-saas-com-ai-visibility-audit.md`.
4. Outputs are saved to:
   - `output/example-saas-com-ai-visibility-audit.md`
   - `output/example-saas-com-ai-visibility-audit.html`
   - `output/example-saas-com-ai-visibility-audit.pdf`

**Expected deliverable:**

- A print-perfect, styled executive PDF featuring modern typography, status pill badges, syntax-highlighted code blocks, running headers/footers, and page-break optimization.

---

## Example 13 — international SEO and hreflang audit

**Skill invoked:** [`international-seo-hreflang-audit`](../skills/ai-visibility/international-seo-hreflang-audit/SKILL.md)

**Prompt:**

> "Audit our multi-regional website `https://example-global.com/` for international AI visibility —
> check whether `/en/`, `/es/`, and `/de/` paths declare bidirectional hreflang tags, valid ISO codes,
> proper self-canonicals, and a working x-default fallback."

**Expected output shape:**

- Target Locale Matrix (URLs, declared hreflang, status codes, canonicals)
- Hreflang Conformance Table (reciprocity status, x-default presence, ISO validity)
- Itemized findings with reproduction commands and remediation code
- Guardrail statement distinguishing observed HTML/header annotations from inferred targeting

---

## Example 14 — developer documentation and API visibility audit

**Skill invoked:** [`docs-api-visibility-audit`](../skills/ai-visibility/docs-api-visibility-audit/SKILL.md)

**Prompt:**

> "Audit our API documentation on `https://api.example.com/docs` to see if AI coding assistants
> (Claude Code, Cursor, Copilot) can parse our REST endpoints — check for discoverable OpenAPI schemas,
> server-side rendered parameter tables, fenced code blocks with language identifiers, and error codes."

**Expected output shape:**

- API Schema Discovery Matrix (probed paths, HTTP status, syntax validity, path count)
- Documentation Renderability & SSR Conformance (raw HTML vs. client-rendered endpoint check)
- Code Sample & Syntax Markup Quality (tagged vs. untagged code blocks)
- Recommended fixes with schema snippets and curl verification commands

---

## Example 15 — paywall and subscription content access audit

**Skill invoked:** [`paywall-access-audit`](../skills/ai-visibility/paywall-access-audit/SKILL.md)

**Prompt:**

> "Audit our subscription publication `https://news.example.com/premium-article` for paywall Schema.org
> compliance, crawlable lead-in snippets, and robots.txt crawler policies (differentiating AI training bots
> from AI search citation bots)."

**Expected output shape:**

- Paywall Specification Conformance Matrix (`isAccessibleForFree` values, `hasPart` cssSelectors)
- Lead-In Snippet Renderability & Visibility (SSR check of introductory paragraph)
- AI Crawler Policy Separation (training bots vs. citation bots in `robots.txt`)
- Recommended Schema.org JSON-LD templates and robots policy adjustments

---

## Example 16 — semantic entity and topical map audit

**Skill invoked:** [`semantic-entity-topical-map-audit`](../skills/ai-visibility/semantic-entity-topical-map-audit/SKILL.md)

**Prompt:**

> "Our brand name collides with several unrelated companies. Audit the entity identity on
> `https://apex.io` — is there a stable `@id`, are there `sameAs` reference pages, do our articles
> reference the canonical organization entity, and are our subtopic pages actually linked from
> their pillar?"

**Expected output shape:**

- Entity Disambiguation & Knowledge Graph Grounding, with a single
  `Entity clarity classification: **AMBIGUOUS | PARTIALLY_GROUNDED | FULLY_RECONCILED**` line
- Schema Graph Reconciliation (canonical `@id` reuse across `Article`/`WebSite`/`Product`, author
  `Person` completeness: `jobTitle`, `worksFor`, `alumniOf`, `sameAs`)
- Topical Map & Cluster Structure (pillar pages, cluster depth, orphan subtopic pages)
- Recommended fixes with copy-pasteable JSON-LD using placeholder Wikidata Q-ids, plus the
  reproducible verification commands that produced each finding

# V3 Scoring Rubric

<!-- Bundled copy of docs/SCORING_RUBRIC.md, kept here so single-skill installs are self-contained (issue #91). Keep both copies in sync when editing either. -->

This is the deduction table the [V3 report template](audit_report_template_v3.md)'s
`Overall Readiness Score` and six pillar scores are derived from. It exists because a bare
`{{PILLAR}}_SCORE/100` with no rubric behind it is false precision: a confident-looking
two-digit number that two auditors (or the same auditor twice) could not reproduce from the
same findings. Every deduction below traces to a specific, real check already run by one of
this pack's specialist skills (see the "Check" column's link into that skill's
`references/checks.md`) — nothing here is a hypothetical or invented check.

## How to apply this rubric

1. Run the specialist skill(s) for the pillar and collect their findings, per that skill's own
   evidence discipline (observed status code, response body, or page text — never inferred).
2. For each check below that is **applicable to this site** (see the "N/A condition" column),
   determine pass/fail (or the graduated condition, where noted) from the findings.
3. Start the pillar at 100. Subtract every triggered deduction. Floor the result at 0. This is
   the pillar's `{{PILLAR}}_SCORE`.
4. If **every** check in a pillar is N/A for this site type, exclude the pillar entirely and
   reweight the remaining pillars (see "Handling inapplicable pillars" below) rather than
   scoring it 0 or 100 by default.
5. The `Overall Readiness Score` is the weight-adjusted sum of the (possibly reweighted) pillar
   scores. Two auditors applying this table to the same finding set must reach the same score;
   if they don't, the finding set — not the rubric — is under-specified and needs a sharper
   pass/fail condition written into this file.

This produces a score that is **traceable**: every point lost has a named check, an observed
finding, and a stated reason it was worth that many points. A reader can always ask "why is
this 62 and not 80?" and get a specific answer back — a subtraction, not a vibe.

## Handling inapplicable checks and pillars

Not every check applies to every site. A documentation site has no `Product`/`Offer` schema to
check; a single-page brochure site may have no FAQ page to test for thinness. Two levels:

- **Check-level N/A**: skip the check, do not count it as a pass or a fail, and do not deduct.
  Note in the report which checks were excluded and why (e.g. "Check 3.2 (Product schema) —
  N/A, site sells no products or services online").
- **Pillar-level N/A**: only when *every* check in the pillar is N/A for this site (this should
  be rare — Discovery and Technical Accessibility apply to every site with a public URL).
  Exclude the pillar from the composite and reweight the rest proportionally:

  ```
  new_weight(i) = old_weight(i) / (1 - excluded_weight_fraction)
  ```

  Example: a docs site where Pillar 6 (Agent/Action Readiness, 5%) is wholly N/A (no forms,
  no conversion path, no commerce actions of any kind exist to check) reweights the remaining
  five pillars from {20, 20, 20, 20, 15} to {21.05, 21.05, 21.05, 21.05, 15.79} (each divided by
  0.95), so they still sum to 100%. State the exclusion and the reweighting explicitly in the
  report — never silently fold an N/A pillar's weight into "full marks" or "zero" for that
  pillar, since both distort the composite in the same way the flat estimate the rubric replaces
  would have.

## Pillar 1 — Discovery (weight: 20%)

Source skills: `robots-ai-crawler-audit`, `sitemap-discovery-audit`, `ecommerce-technical-seo-audit`
(catalog-specific crawl-path checks 1.9-1.11, ecommerce sites only), `international-seo-hreflang-audit`
(multilingual/multi-region check 1.12).

| # | Check | Tier | Deduction | N/A condition | Rationale |
|---|---|---|---|---|---|
| 1.1 | `robots.txt` has `Disallow: /` under a named major AI-crawler user-agent (GPTBot, ClaudeBot, PerplexityBot, Amazonbot) | Critical Foundation | −25 per distinct blocked crawler family, capped at −50 total | Never — every public site has a `robots.txt` fetch outcome | A full-site `Disallow` for a named AI crawler doesn't degrade the crawler's view of the site, it eliminates it — the crawler never sees a single page. This is the single most severe, unambiguous blocker the pillar can find, so it gets the largest weight in the pillar and is capped rather than allowed to zero the pillar on its own, since a site that blocks 3 named bots isn't 3x worse than one that blocks 1 in a way a human reader would find intuitive. |
| 1.2 | Live fetch as a bot user-agent returns a different status (403/429/redirect) than a default UA fetch of the same URL | Critical Foundation | −25 | Never | An edge/WAF-level block is invisible to a `robots.txt` read alone and is just as total a blocker as an explicit `Disallow` — evidenced by the differential status code, not an assumption. |
| 1.3 | `sitemap.xml` / `sitemap_index.xml` returns non-2xx at both conventional paths and isn't declared (or is declared but 404s) in `robots.txt` | Important Improvement | −15 | Never | No sitemap doesn't block crawling outright (a crawler can still discover pages via links), but it removes the fastest, most reliable discovery path and is a documented Tier-2 example in the V3 design doc. |
| 1.4 | Sitemap fetch succeeds but is not well-formed XML (fails `xml.dom.minidom.parseString`) | Important Improvement | −10 | Never | A malformed sitemap is worse than a missing one in one respect — it may be silently ignored or partially parsed by different consumers, giving inconsistent discovery results. |
| 1.5 | ≥10% of sampled sitemap URLs return non-2xx | Important Improvement | −1 per 10% of sampled URLs broken, capped at −10 | N/A if sitemap itself is absent (already penalized under 1.3) | Sitemap entries returning dead links tell a crawler the sitemap is unreliable, discounting trust in every other entry too — scaled by proportion rather than a flat penalty because a site with 2 stale URLs out of 500 is a materially different problem than one with half its sitemap broken. |
| 1.6 | Canonical `<link rel="canonical">` on a sampled key page is missing or points to a different URL (non-self-referential without documented reason, e.g. cross-domain duplicate) | Important Improvement | −10 | Never | Ambiguous or absent canonicalization can cause a search/AI system to index or cite the wrong URL, or split authority across duplicates. |
| 1.7 | Nav/footer-linked pages are absent from the sitemap (via the nav-vs-sitemap `comm` diff) | Supporting Signal | −5 | N/A if sitemap itself is absent (already penalized under 1.3) | A coverage gap here is a hygiene issue, not a foundational blocker — the pages are still reachable by a crawler that follows links, just missing the fast path. |
| 1.8 | Broken internal links found during the homepage/nav crawl sweep, independent of sitemap membership | Supporting Signal | −5 | Never | Degrades crawl paths and user/agent trust but doesn't itself block discovery of the rest of the site. |
| 1.9 | A sampled category/collection page's faceted-navigation variant (filter/sort query parameter) returns `200`, has no canonical back to the base URL, has no `noindex`, and is not blocked in `robots.txt` (`ecommerce-technical-seo-audit` check) | Important Improvement | −10 | N/A if the site has no faceted/filterable category navigation (e.g. non-ecommerce site, or a catalog with no filter/sort UI) | Per Google's own faceted-navigation guidance cited in the skill's `checks.md`, an uncanonicalized, indexable facet URL is a crawlable near-duplicate of the base category page that dilutes crawl budget across "a very large number" of parameter combinations — a real index-quality problem, but the base category page itself still resolves and is indexable, so this sits at the same Important tier and weight as 1.6's canonicalization check rather than at Critical Foundation, since no page is made unreachable. |
| 1.10 | A sampled URL present in the sitemap has no discoverable internal link pointing to it from nav, category grids, or related-content blocks (orphan page, per `ecommerce-technical-seo-audit`'s sitemap-vs-crawled-links diff) | Supporting Signal | −5 | N/A if sitemap itself is absent (already penalized under 1.3) or the orphan-page cross-reference check wasn't run | An orphan page is still reachable via the sitemap's fast path, it's only missing the slower reinforcement of an internal link — the mirror image of 1.7's nav-without-sitemap gap and weighted identically for the same reason: a coverage/reinforcement hygiene issue, not a foundational block. |
| 1.11 | A sampled discontinued/out-of-season product URL returns a `200` with error/out-of-stock page content (soft 404), or redirects to the homepage or an unrelated category instead of the closest matching replacement product/category, per `ecommerce-technical-seo-audit`'s check | Important Improvement | −15 | N/A if the site has no discontinued or out-of-season products to sample | Per Google's own soft-404 documentation cited in the skill's `checks.md`, this failure mode wastes crawl budget on a dead page and discards whatever ranking/citation signal the original URL had built up — a real, page-scoped resolution failure, so it is weighted the same as 1.3's missing-sitemap check (a comparable "the expected resolution path is broken" severity) rather than at Critical Foundation, since it affects one product's URL rather than blocking crawl access to the site as a whole. |
| 1.12 | A multilingual or multi-regional site has broken bidirectional hreflang tags, missing x-default fallback, invalid ISO language/country codes, or sitemap hreflang mismatches (`international-seo-hreflang-audit` check) | Important Improvement | −10 | N/A if the site is single-language and single-region (no alternate locales served) | Per Google Search Central hreflang guidelines `[GOOGLE-HREFLANG-01]`, broken return links or invalid language codes prevent search engines and AI answer engines from routing users to the appropriate language/regional variation. Single-language sites have no alternate variations and are not penalized. |
| 1.13 | `robots.txt` has `Disallow: /` under an AI-training opt-out token or training-data crawler (Google-Extended, Applebot-Extended, CCBot) | Supporting Signal | −5 total | Never — every public site has a `robots.txt` fetch outcome | `Google-Extended` has no separate HTTP user-agent and does not affect Google Search inclusion or ranking `[GOOGLE-EXTENDED-01]`; `Applebot-Extended` controls training use without removing pages from Applebot-powered search `[APPLE-BOTS-01]`; CCBot supplies a general-purpose web corpus rather than a direct answer-engine citation surface `[COMMONCRAWL-CCBOT-01]`. Treat these as a reported training-policy signal, not a critical discovery outage. |

## Pillar 2 — Technical Accessibility (weight: 20%)

Source skills: `robots-ai-crawler-audit` (page-level directives), `answer-engine-content-audit`
(server-rendered content), `image-audit` (fetchability).

| # | Check | Tier | Deduction | N/A condition | Rationale |
|---|---|---|---|---|---|
| 2.1 | Heading/body text present in the rendered browser DOM is absent from the raw `curl`'d HTML (client-side-only rendering) | Critical Foundation | −30 | Never | Most AI crawlers (GPTBot, ClaudeBot, PerplexityBot) do not execute JavaScript. If the substantive content only exists after JS runs, the crawler sees an empty shell — this is the technical-accessibility equivalent of 1.1's total block, just at the content layer instead of the access layer. |
| 2.2 | `X-Robots-Tag: noindex` header or `<meta name="robots" content="noindex">` present on a sampled key page | Critical Foundation | −25 | Never | An explicit noindex is a direct, deliberate instruction telling every compliant crawler to exclude the page — full weight because it is unambiguous and page-scoped rather than inferred. |
| 2.3 | A sampled key/claim page returns a non-2xx status or sits behind an unresolved 3xx redirect chain | Critical Foundation | −20 | Never | A page that doesn't resolve cleanly can't be read at all regardless of its content quality. |
| 2.4 | Critical on-page image has only a JS-driven `data-src`/`data-lazy` attribute with no fallback `src` and no `<noscript>` fallback | Important Improvement | −15 | N/A if the page under review has no images material to understanding it (e.g. a pure-text docs page) | Per `image-audit`'s checks.md, this is unreachable to a non-JS-executing agent regardless of how it renders in a real browser — a real but narrower gap than 2.1 since it affects specific assets, not the whole page's text. |
| 2.5 | Sampled key page has no `<h1>`, multiple competing `<h1>`s, or a heading hierarchy that skips levels (e.g. `<h1>` → `<h3>`) | Important Improvement | −10 | Never | Semantic heading structure is how a non-visual parser infers document outline and importance; a broken hierarchy makes automated section-extraction unreliable. |
| 2.6 | Lighthouse-sourced Core Web Vitals (LCP) fails Google's "poor" threshold on a sampled key page | Supporting Signal | −10 | N/A if no Lighthouse/PSI data was collected for this audit | Slow delivery affects user and crawl-budget experience but does not, on its own, prevent a page from being read once fetched — consolidated here per the V3 design doc's Lighthouse-mapping table rather than shown as a duplicate parallel score. |
| 2.7 | Lighthouse Accessibility score falls in the "needs improvement" band on a sampled key page, for issues not already covered by 2.4/2.5 | Supporting Signal | −5 | N/A if no Lighthouse/PSI data was collected for this audit | Genuine quality signal, but per the V3 design doc Tier-3 examples ("non-critical accessibility improvements") it must not outweigh the pillar's foundational checks. |
| 2.8 | A `<title>`, `<meta name="description">`, `<link rel="canonical">`, or JSON-LD block is present in the hydrated DOM (headless `--dump-dom`) but absent from the initial server response | Important Improvement | −15 | N/A if the raw and hydrated passes agree, or if no hydrated-DOM pass could be run (no Chromium-family browser available) — in that case 2.8 itself is N/A because the divergence cannot be observed, but the underlying items are still scored from the raw pass and labelled `[Derived]` with a "no browser available, hydration cross-check not performed" disclosure, so items whose N/A column reads "Never" stay reachable | The metadata exists and a JS-executing client sees it, so this is not the total content blackout 2.1 penalizes — but non-JS-executing crawlers (GPTBot, ClaudeBot, PerplexityBot) still receive a page with no title, description, canonical, or structured data. Scored here in the delivery pillar rather than as a Pillar 3/4 absence, so the same gap is never counted twice. |

## Pillar 3 — Machine Understanding (weight: 20%)

Source skills: `schema-markup-audit`, `docs-api-visibility-audit` (API platform check 3.7), `paywall-access-audit` (paywall check 3.8).

| # | Check | Tier | Deduction | N/A condition | Rationale |
|---|---|---|---|---|---|
| 3.1 | No canonical `Organization` JSON-LD entity found site-wide (checked on homepage/footer-linked about page) | Important Improvement | −25 | Never — every business site has an identity to declare. With no hydrated-DOM pass available, score it from the raw pass and label the finding `[Derived]` (see 2.8); it is never withheld | `Organization` schema is the anchor entity every other structured claim (author, product, service) attaches to via `publisher`/`brand`/`sameAs`. Its absence is explicitly named as a Tier-2 example in the V3 design doc, and it's the single highest-value schema check in this pillar because everything else compounds on top of it. |
| 3.2 | No `Product`, `Service`, or `SoftwareApplication` schema for the site's primary paid offering, where the site type has one | Important Improvement | −20 | N/A if the site has no product, service, or software offering to schema-mark (e.g. a personal blog, a pure documentation site) | This is the schema that lets an agent extract price, availability, and category without reading prose — its absence blocks a specific, high-value machine action (price/availability extraction), which is why it is weighted just under `Organization` itself. |
| 3.3 | A present `Product`/`Service`/`Organization` entity is missing a required property per `checks.md`'s property checklist (e.g. `Product` missing `offers.price` or `offers.availability`; `Organization` missing `contactPoint`) | Important Improvement | −15 | N/A if the corresponding entity type (3.1/3.2) isn't present at all — already fully penalized above | An incomplete entity is a partial win, not a full one: the type declaration exists, but the specific property an agent would query (price, availability, contact route) is still absent. |
| 3.4 | A schema-claimed property doesn't match the visible page text it purports to describe (e.g. schema price differs from displayed price) | Critical Foundation | −20 | N/A if no comparable schema property exists to check against page text | Per this pack's cross-check convention, a mismatch is worse than an absence — it's a concrete source of hallucination risk where an AI system could confidently cite a wrong number, rather than simply having nothing to cite. |
| 3.5 | `FAQPage` schema's `Question`/`acceptedAnswer` pairs don't match the visible on-page Q&A verbatim | Important Improvement | −10 | N/A if no `FAQPage` schema is present (nothing to mismatch) | Same mismatch principle as 3.4 but scoped to FAQ content specifically and weighted lower since FAQ answers are typically lower-stakes than pricing/availability facts. |
| 3.6 | No `sameAs` links (verified social/profile/authority URLs) on the `Organization` entity | Supporting Signal | −10 | N/A if 3.1 already failed (nothing to attach `sameAs` to) | `sameAs` helps disambiguate the entity against other same-named organizations but isn't itself required for basic identification — a genuine but secondary signal, consistent with the V3 design doc listing `sameAs` under "may include" rather than a hard requirement. |
| 3.7 | A developer portal, API platform, or SDK guide site has no discoverable, parseable OpenAPI/Swagger specification at conventional paths or `<link rel="describedby">` (`docs-api-visibility-audit` check) | Important Improvement | −15 | N/A if the site is not a developer portal, API provider, or SDK platform | Per OpenAPI specifications `[OPENAPI-SPEC-01]`, machine-readable API definitions allow AI coding agents to understand parameter models, endpoints, and response schemas without fragile HTML scraping. Non-developer sites have no APIs and are not penalized. |
| 3.8 | A subscription-gated or paywalled page lacks Schema.org `isAccessibleForFree` specification markup or has mismatched `hasPart` cssSelectors (`paywall-access-audit` check) | Critical Foundation | −20 | N/A if the site does not contain paywalled or subscription-gated content | Per Google and Schema.org paywall specifications `[GOOGLE-PAYWALL-SCHEMA-01]` `[SCHEMA-ISACCESSIBLEFORFREE-01]`, paywalled content must explicitly declare `isAccessibleForFree: "False"` and valid `hasPart` selectors to prevent search engines from penalizing the gated text as cloaking. Free and open access sites are not penalized. |

## Pillar 4 — Answer Readiness (weight: 20%)

Source skills: `answer-engine-content-audit`, `robots-ai-crawler-audit`,
`ecommerce-technical-seo-audit` (catalog-specific extractability check 4.7,
ecommerce sites only).

| # | Check | Tier | Deduction | N/A condition | Rationale |
|---|---|---|---|---|---|
| 4.1 | FAQ/Q&A content exists structurally (a dedicated FAQ section or page) but the answer text is placeholder, boilerplate, or otherwise substantively empty (e.g. Lorem Ipsum, answers under ~20 characters) | Critical Foundation | −25 | N/A if the site has no FAQ/Q&A section at all (see 4.3 instead) | This is the single worst answer-readiness failure this pillar can find: the site has visibly signaled "here is where we answer your question" and then not actually answered it — worse than having no FAQ section, since it invites a citation that then fails to hold up, and it is explicitly the failure mode named in this rubric's own motivating example. |
| 4.2 | A pricing/comparison-intent page (URL or heading suggests pricing, "vs", or comparison) contains no dollar figure and no comparison language (`vs`, `versus`, `compared to`, `alternative`) | Important Improvement | −15 | N/A if the site has no pricing/comparison-intent page | Pricing and comparison questions are among the highest-frequency AI-answer triggers per this skill's checks.md; a page that exists specifically for this intent and doesn't deliver it is a direct answer-readiness gap, not a general content-quality nitpick. |
| 4.3 | No heading on any candidate answer page (FAQ, pricing, docs, guide, support, compare) is phrased as a direct question (`what`/`how`/`why`/`when`/`is`/`can`/`does`) | Important Improvement | −15 | N/A if the site has no candidate answer pages at all (e.g. a pure single-page brochure with no FAQ/docs/support/guide content) | Question-phrased headings are what make a passage easy for an answer engine to lift and cite verbatim; their total absence across all candidate pages means every answer must be inferred from prose rather than extracted directly. |
| 4.4 | `<title>` on a sampled key page is missing, or present but over ~60 characters (truncation-risk "vague" per Ahrefs' pixel-width research, `[AHREFS-TITLE-LENGTH-01]`) | Important Improvement | −10 missing / −5 vague | Never | The title is verbatim text an answer engine or search snippet quotes back to the user — missing it removes the primary citation label; an overlong one risks being cut mid-word, which is a real but smaller degradation. |
| 4.5 | Meta description on a sampled key page is missing, or present but empty/boilerplate/over ~160 characters ("vague") | Supporting Signal | −5 missing / −3 vague | Never | Per the task's own calibration example, this is "a minor citation-quality signal" — it affects how a snippet reads, not whether the underlying content can be found or understood, so it sits well below the title check and the structural answer checks above. |
| 4.6 | No freshness signal (`article:published_time`/`article:modified_time` meta, or a visible "updated"/"last modified" string) on time-sensitive content (pricing, docs, guides) | Supporting Signal | −10 | N/A if the sampled content is genuinely evergreen with no freshness claim to make (rare — most business content benefits from a dateline) | Freshness is a supporting trust/recency signal, not a blocker to extracting the answer itself, consistent with its Tier-3 framing in the V3 design doc's "content freshness" example. |
| 4.7 | A sampled category/collection page has under ~300 words of unique, non-boilerplate, non-product-grid text *and* that text duplicates another category's copy (`ecommerce-technical-seo-audit`'s two-part thin-content test) | Important Improvement | −10 per flagged sampled page, capped at −20 | N/A if the site has no category/collection page structure (e.g. a single-product store or a non-ecommerce site) | A category page this thin gives an agent nothing distinct to extract or cite about that specific category — it can only paraphrase the product grid or fall back to a near-identical sibling page's copy. This is a real but non-catastrophic extractability gap, not the "promised then empty" failure of 4.1 (a dedicated FAQ section is a much stronger, explicit signal to a reader that an answer exists here), so it sits at the same Important tier and weight as 4.2/4.3 rather than 4.1's Critical tier. The check requires *both* low word count and duplication, per the skill's own guardrail against flagging a page as thin from word count alone (a low count can be a legitimate short category with no duplication problem) and against extrapolating a small sample into a catalog-wide count — the −20 cap keeps a 3-5 page sample from swinging the pillar further than the sample itself justifies. |
| 4.8 | `<meta name="robots">`, `<meta name="googlebot">`, or `X-Robots-Tag` contains `nosnippet` or `max-snippet:0` on a sampled key page | Critical Foundation | −25 | Never | Google requires a page to be eligible for a snippet before it can appear as a supporting link in AI Overviews or AI Mode; `nosnippet` and the equivalent `max-snippet:0` prevent that eligibility and direct-input use `[GOOGLE-AI-FEATURES-01]` `[GOOGLE-ROBOTS-META-01]`. This is an explicit page-level answer exclusion, but it also suppresses classic Google Search text snippets; report the trade-off and confirm the site's intended content policy rather than blindly recommending removal. |

## Pillar 5 — Trust & Authority (weight: 15%)

Source skill: `citation-readiness-audit`.

| # | Check | Tier | Deduction | N/A condition | Rationale |
|---|---|---|---|---|---|
| 5.1 | A specific claim's canonical URL 3xx-redirects unresolved, has a non-self-referential canonical, or carries `noindex` | Critical Foundation | −25 | Never | Per `citation-readiness-audit`'s checks.md, this is an explicit blocker — a claim living on a URL that isn't stable or indexable cannot be treated as citable at all, regardless of how good the claim text itself is. |
| 5.2 | The claim's exact text does not appear in the server-rendered page content (client-rendered only, or not actually present) | Critical Foundation | −25 | Never | Same severity class as 5.1 for the same reason: per the skill's own rule, a claim that fails this check "must not be marked citable," so it caps the pillar as hard as an unstable URL does. |
| 5.3 | No identifiable `Organization`/`Person` schema entity backs the claims on the site | Important Improvement | −20 | Never | Without a named entity, an AI system has nothing concrete to attribute a citation to — this overlaps with Pillar 3's check 3.1 by design (both skills independently surface the same gap) and per the unified-finding model should be reported as one canonical finding citing both pieces of evidence, not scored twice as if they were unrelated. |
| 5.4 | No author or leadership attribution (`author`/`by`-line pattern) found on content pages | Important Improvement | −15 | N/A if the site type has no individually-authored content (e.g. a pure product catalog with no blog/articles) | Named authorship is a documented trust signal for content-based claims specifically, distinct from the organization-level entity check in 5.3. |
| 5.5 | `/contact` and `/support` (or site-declared equivalents) both return non-2xx | Important Improvement | −15 | N/A if the site is not customer-facing in a way that implies a contact path should exist (rare) | A working contact/support path is this skill's own "baseline trust signal" check — its total absence means there is no verifiable human accountability behind the site's claims. |
| 5.6 | No freshness signals (`article:published_time`/`modified_time`, visible "updated"/"effective date") on claim pages | Supporting Signal | −10 | N/A if claim content is genuinely evergreen | Stale, undated claims are a weaker trust signal than an active, dated one, but a claim can still be accurate and citable without a visible date — hence supporting rather than blocking. |
| 5.7 | No case studies, testimonials, or quantified client results found anywhere on the site | Supporting Signal | −10 | N/A if the site type doesn't plausibly carry case studies (e.g. an internal tool's public docs site) | Case studies strengthen confidence in claims but their absence doesn't make existing claims false or uncitable — a supporting enhancement, not a foundational trust requirement. |

## Pillar 6 — Agent/Action Readiness (weight: 5%)

Source skills: `citation-readiness-audit` (contact path), `schema-markup-audit` (actionable
`Offer`/`Product` data). This pillar's weight is intentionally the smallest of the six —
per the V3 design doc, emerging agent protocols such as `llms.txt` are Tier 4 and must never
affect this score; only checks with a real, present-day mechanism (a working form, a
machine-readable price) are scored here.

| # | Check | Tier | Deduction | N/A condition | Rationale |
|---|---|---|---|---|---|
| 6.1 | No working conversion/action endpoint at all (`/contact`, `/support`, a booking or checkout path all return non-2xx) | Important Improvement | −40 | Never | With no reachable action endpoint, an agent has literally nothing to act on regardless of how well everything else scores — this is the pillar's own version of a total blocker, sized to dominate its small 5%-weighted pillar the way 1.1 dominates Discovery. |
| 6.2 | No machine-readable price/availability data (`Offer`/`priceSpecification`/`Product.offers`) exists for a site that sells something, forcing an agent to infer price from prose | Important Improvement | −40 | N/A if the site has nothing to transact (no products, services, or bookable actions) | This duplicates evidence with Pillar 3 check 3.2/3.3 by design — the unified-finding model should present it as one canonical finding with two pillar tags (Machine Understanding *and* Agent/Action Readiness) rather than inventing a separate Pillar-6-only check, since the same missing schema blocks both understanding and agentic action. |
| 6.3 | A conversion form exists but its inputs have no associated `<label>`/`name`/`required` semantics, making the form's purpose and required fields un-parseable without visual rendering | Supporting Signal | −15 | N/A if the site has no forms (e.g. contact is a plain mailto/phone link) | A structurally opaque form degrades an agent's ability to fill it out correctly but doesn't remove the conversion path entirely the way 6.1 does. |
| 6.4 | No documentation, pricing, or process page is discoverable that would let an agent understand *how* to engage (steps, requirements, pricing tiers) before acting | Supporting Signal | −15 | N/A if the site's engagement model is a single obvious action with no process to document (e.g. a single "Buy Now" button with no onboarding steps) | Useful for agent confidence before it acts, but its absence doesn't block the action itself the way 6.1's missing endpoint does. |

## Skills intentionally excluded from scoring

Two of this pack's specialist skills produce findings that never appear in the deduction tables
above, on purpose. Both are stated here explicitly rather than left silently absent, per this
rubric's own discipline (see "Handling inapplicable checks and pillars" above).

- **`llms-txt-generator`** — `llms.txt` presence, validity, and correct `Content-Type` (a real
  `text/plain` file vs. a JS-shell/SPA-fallback false positive) is never scored, in any pillar.
  This isn't an oversight this issue is fixing — it's an explicit, already-shipped design
  decision: the pack's top-level `docs/AUDIT_REPORTING_GUIDE.md` (a repo-root doc, not bundled in
  this skill's own `references/`) — its four-tier evidence hierarchy names `llms.txt` by
  name as a Tier 4 "Experimental Protocol" and states as a "Mandatory Rule" that "Tier 4 items
  *never* reduce the core 100-point audit score," and Pillar 6's own rationale text above
  repeats the same rule for the same reason. `llms.txt` is a community draft convention
  (llmstxt.org) with no confirmed adoption by the major AI crawlers this pack audits against —
  unlike `robots.txt` and `sitemap.xml`, which are long-established, universally-respected
  standards this rubric does score. Wiring `llms-txt-generator`'s findings into a pillar would
  directly contradict that already-documented mandatory rule rather than close a gap, so its
  findings stay exactly where `audit_report_template_v3.md` already places them:
  Section 6, "[EXPERIMENTAL] Emerging Agent Protocols (Draft Standards)" — reported, but
  explicitly non-scoring.
- **`commerce-protocol-discovery`** — none of its four discovery probes (UCP business profile,
  A2A Agent Card, protected MCP endpoint challenge, catalog feed) appear in any pillar's
  deduction table. Per the skill's own `SKILL.md` and Guardrails, this is a **discovery-only
  teaser by explicit design**, not an oversight: it is mechanically forbidden from using
  `ready`/`partial`/`missing`/`verified` or any other graded-assessment language, and its own
  eval enforces this via regex contract checks rather than a scoring table. Full
  commerce-protocol *readiness* scoring (a graded rubric, trust/order-lifecycle gates, and
  remediation guidance) is explicitly named in the skill's own description as a separate, deeper
  audit capability this skill does not attempt — inventing a scoring path for it here would
  duplicate or pre-empt that separate capability and would contradict the one skill in this pack
  whose entire design purpose is to *not* be scored. Its findings are reported as-is (protocol
  probed, endpoint, observed status) with no pillar attribution and no contribution to the
  Overall Readiness Score.

## Worked example

A SaaS marketing site audit finds: `robots.txt` blocks `GPTBot` entirely (1.1, −25); sitemap
exists and is healthy (no deduction); no `Organization` schema anywhere (3.1, −25); the
`/pricing` page has dollar figures and comparison copy (no deduction, 4.2 passes); the site's
FAQ page answers are all real content (4.1 N/A-pass); meta description on `/pricing` is missing
(4.5, −5); `/contact` returns `200` (no deduction).

- **Discovery**: 100 − 25 = **75**
- **Machine Understanding**: 100 − 25 = **75**
- **Answer Readiness**: 100 − 5 = **95**
- **Trust & Authority, Technical Accessibility, Agent/Action Readiness**: no triggered checks
  found in this abbreviated example → 100 each (in a real audit these would still need every
  applicable check run and recorded, not assumed clean by default)

This is a SaaS marketing site with no catalog, so `ecommerce-technical-seo-audit`'s checks
(1.9-1.11, 4.7) are all check-level N/A — no category/collection pages, no faceted navigation,
no discontinued products to sample — and contribute no deduction, exactly as check-level N/A
checks do everywhere else in this rubric. This doesn't change the math below; it's recorded here
so the new checks aren't silently absent from the worked example the way the "Handling
inapplicable checks" section above requires N/A checks to be stated, not omitted.

Overall = (75×0.20) + (100×0.20) + (75×0.20) + (95×0.20) + (100×0.15) + (100×0.05)
= 15 + 20 + 15 + 19 + 15 + 5 = **89/100**

Re-running this exact finding set through this table, by a different person or the same person
a week later, must produce 89 again — that reproducibility is the entire point of replacing a
free-form estimate with this table.

## What this rubric does not do

It does not, and cannot, predict whether ChatGPT, Perplexity, or any other AI system will
actually cite or recommend the audited site — that is a live-platform outcome this pack
explicitly treats as out of scope for a static crawl-based audit (see the pack's top-level
`docs/RUNNING_AN_AUDIT.md`, a repo-root doc not bundled in this skill's own `references/`).
What it produces is a reproducible score
for the audited *readiness signals* — the same category of claim a Lighthouse or PageSpeed
score makes about performance, not a citation or ranking guarantee.

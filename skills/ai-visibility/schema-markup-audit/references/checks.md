# Schema markup extraction and property checklists

## Extract structured data

Match `application/ld+json` anywhere inside the `<script>` tag, never as an adjacent token
straight after `<script` — an `id`, `nonce`, or framework attribute in front of `type=` is
common, and an adjacent-token pattern silently misses those blocks.

```bash
curl -s "$URL" | grep -oiE '<script[^>]+application/ld\+json[^>]*>[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
curl -s "$URL" | grep -oiE 'itemtype="[^"]*"' | sort -u
```

### Hydrated-DOM re-check when the raw pass finds nothing

Zero JSON-LD blocks in the raw response is an unresolved check, not a finding. Frameworks
serialize schema into a streaming payload (Next.js App Router: `self.__next_f.push(...)`, often
including a block injected via `dangerouslySetInnerHTML`) or inject it during hydration (React
Helmet), so it exists only after JavaScript has run. Headless Chromium already ships as a
dependency of this pack (`scripts/render-audit-pdf.py`), so the second pass needs no new tooling:

```bash
CHROME=$(command -v google-chrome || command -v chromium || command -v chromium-browser)
"$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$URL" > /tmp/hydrated.html
grep -oiE '<script[^>]+application/ld\+json[^>]*>' /tmp/hydrated.html | wc -l
python3 -c "
import json, re, sys
html = open('/tmp/hydrated.html', encoding='utf-8', errors='replace').read()
blocks = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I)
print(f'{len(blocks)} JSON-LD block(s) in hydrated DOM')
for block in blocks:
    try:
        print(json.loads(block).get('@type'))
    except json.JSONDecodeError as exc:
        print(f'unparseable block: {exc}')
"
```

Report the comparison, not just the pass that found something:

- **raw 0 / hydrated 0** — genuinely no structured data; report as missing.
- **raw 0 / hydrated N** — the entities exist, so never report them missing. Report them as
  present in the rendered DOM but absent from the initial server response, therefore invisible
  to non-JS-executing crawlers (GPTBot, ClaudeBot, PerplexityBot), and audit the blocks'
  properties as normal on top of that delivery finding.
- **raw N / hydrated M** with `M > N` — some blocks are server-rendered and others are not; say
  which are which rather than reporting a single count.

Cite both observations (the `curl` count and the `--dump-dom` count) so the delivery conclusion
is reproducible by whoever implements the fix.

List all `@type` values found:

```bash
curl -s "$URL" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -c "
import json,sys
def types(o):
    if isinstance(o,dict):
        t=o.get('@type');
        if t: print(t)
        [types(v) for v in o.values()]
    elif isinstance(o,list): [types(v) for v in o]
for block in sys.stdin.read().split('\n'):
    try: types(json.loads(block))
    except Exception: pass
"
```

## Property checklists by page type

- **Product** [SCHEMA-PRODUCT-01]: `name`, `image`, `description`, `sku` or `gtin`, `brand`, `offers.price`, `offers.priceCurrency`, `offers.availability`; variants via `hasVariant` or per-variant offers; `aggregateRating`/`review` only if visible on page.
- **Organization** [SCHEMA-ORGANIZATION-01]: `name`, `url`, `logo`, `sameAs` (social/profile links), `contactPoint`; one canonical Organization entity site-wide, not one per page.
- **Article/BlogPosting** [SCHEMA-ARTICLE-01]: `headline`, `datePublished`, `dateModified`, `author` (Person with `name`, ideally `url`), `publisher`.
- **FAQPage** [SCHEMA-FAQPAGE-01]: each `Question`/`acceptedAnswer` pair must match visible on-page Q&A verbatim.
- **BreadcrumbList** [SCHEMA-BREADCRUMBLIST-01]: `itemListElement` positions match the visible trail; URLs absolute and canonical.
- **LocalBusiness** [SCHEMA-LOCALBUSINESS-01]: `name`, `address` (PostalAddress), `geo`, `openingHoursSpecification`, `telephone`; type as specific as truthful (`Restaurant`, not `LocalBusiness`).
- **SoftwareApplication** [SCHEMA-SOFTWAREAPPLICATION-01]: `name`, `applicationCategory`, `operatingSystem`, `offers` (including free = price 0).

## Verification

- Rich results eligibility: https://search.google.com/test/rich-results
- Generic validation: https://validator.schema.org
- Cross-check every claimed property against visible page content; flag any schema-only claims as mismatches.

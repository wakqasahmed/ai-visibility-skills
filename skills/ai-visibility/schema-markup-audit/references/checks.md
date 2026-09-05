# Schema markup extraction and property checklists

## Extract structured data

Match `application/ld+json` anywhere inside the `<script>` tag, never as an adjacent token
straight after `<script` — an `id`, `nonce`, or framework attribute in front of `type=` is
common, and an adjacent-token pattern silently misses those blocks.
Define the extractor once in the audit shell; it accepts a file path or reads stdin when the
path is omitted, so the raw and hydrated passes use identical matching semantics.

```bash
extract_json_ld() {
  python3 -c '
import json, re, sys
source, mode = sys.argv[1:]
html = open(source, encoding="utf-8", errors="replace").read() if source else sys.stdin.read()
blocks = re.findall(r"<script[^>]+application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I)
print(f"{len(blocks)} JSON-LD block(s)")
def types(value):
    if isinstance(value, dict):
        if "@type" in value:
            print(value["@type"])
        for child in value.values():
            types(child)
    elif isinstance(value, list):
        for child in value:
            types(child)
for block in blocks:
    try:
        data = json.loads(block)
        types(data) if mode == "types" else print(json.dumps(data, indent=2))
    except json.JSONDecodeError as exc:
        print(f"unparseable JSON-LD block: {exc}")
' "${1:-}" "${2:-json}"
}

curl -s "$URL" | extract_json_ld
curl -s "$URL" | grep -oiE 'itemtype="[^"]*"' | sort -u
```

### Hydrated-DOM re-check when the raw pass finds nothing

Zero JSON-LD blocks in the raw response is an unresolved check, not a finding. Frameworks
serialize schema into a streaming payload (Next.js App Router: `self.__next_f.push(...)`, often
including a block injected via `dangerouslySetInnerHTML`) or inject it during hydration (React
Helmet), so it exists only after JavaScript has run. The second pass needs a local
Chromium-family browser; the pack does not pin one (`scripts/render-audit-pdf.py` only
auto-detects whichever of Chrome/Edge/Chromium is installed), so detect it and handle its
absence explicitly:

This skill owns the scratch directory created below. Do not reuse it for another skill; a
multi-skill run must not cross-contaminate hydrated-page evidence.

```bash
WORK=$(mktemp -d)
CHROME=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium \
  || command -v chromium-browser || command -v microsoft-edge || true)
if [ -z "$CHROME" ]; then
  echo "no Chromium-family browser available, hydration cross-check not performed"
  exit 0
fi
"$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$URL" > "$WORK"/schema-markup-audit-hydrated.html
grep -oiE '<script[^>]+application/ld\+json[^>]*>' "$WORK"/schema-markup-audit-hydrated.html | wc -l
# extract_json_ld is defined in the "Extract structured data" fence above, but
# each ```bash fence is a separately-invoked shell — the function is not in
# scope here, so it is redefined rather than called across fences.
extract_json_ld() {
  python3 -c '
import json, re, sys
source, mode = sys.argv[1:]
html = open(source, encoding="utf-8", errors="replace").read() if source else sys.stdin.read()
blocks = re.findall(r"<script[^>]+application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I)
print(f"{len(blocks)} JSON-LD block(s)")
def types(value):
    if isinstance(value, dict):
        if "@type" in value:
            print(value["@type"])
        for child in value.values():
            types(child)
    elif isinstance(value, list):
        for child in value:
            types(child)
for block in blocks:
    try:
        data = json.loads(block)
        types(data) if mode == "types" else print(json.dumps(data, indent=2))
    except json.JSONDecodeError as exc:
        print(f"unparseable JSON-LD block: {exc}")
' "${1:-}" "${2:-json}"
}
extract_json_ld "$WORK"/schema-markup-audit-hydrated.html types
```

Report the comparison, not just the pass that found something:

- **raw 0 / hydrated 0** — genuinely no structured data; report as missing.
- **raw 0 / hydrated N** — the entities exist, so never report them missing. Report them as
  present in the rendered DOM but absent from the initial server response, therefore invisible
  to non-JS-executing crawlers (GPTBot, ClaudeBot, PerplexityBot), and audit the blocks'
  properties as normal on top of that delivery finding.
- **raw N / hydrated M** with `M > N` — some blocks are server-rendered and others are not; say
  which are which rather than reporting a single count.
- **raw 0 / no browser available** — unresolved, not missing. Report it as `[Derived]` with the
  words "no browser available, hydration cross-check not performed"; never write it up as either
  present or absent.

Cite both observations (the `curl` count and the `--dump-dom` count) so the delivery conclusion
is reproducible by whoever implements the fix.

List all `@type` values found:

```bash
curl -s "$URL" | extract_json_ld /dev/stdin types
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

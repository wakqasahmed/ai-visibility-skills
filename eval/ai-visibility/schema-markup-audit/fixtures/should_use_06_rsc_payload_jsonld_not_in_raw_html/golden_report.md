## Existing schema types found

You do have structured data — four blocks, all of them delivered only after hydration:

| Type | Raw HTML (`curl`) | Hydrated DOM (`--dump-dom`) |
|---|---|---|
| `Organization` (`id="homepage-jsonld"`, injected via `dangerouslySetInnerHTML`) | absent | present |
| `FAQPage` (7 Q&A pairs) | absent | present |
| `BreadcrumbList` ×2 | absent | present |

The raw pass matched 0 blocks because the markup is serialized into the Next.js RSC streaming
payload (`self.__next_f.push(...)`, 214 chunks) rather than served as static `<script>` tags in
the initial server response. Crawlers that do not execute JavaScript — GPTBot, ClaudeBot,
PerplexityBot — receive a page with no structured data at all, even though a browser sees four
valid blocks.

This is a delivery finding, not a missing-schema finding. The entities exist and are correct;
they just are not in the bytes a non-JS-executing agent reads.

## Missing or weak schema

- `Organization` has only `name` and `url`. `logo` is visible on the page
  (`https://northwind-labs.example/logo.svg`) and `sameAs` profile links are in the footer
  (LinkedIn, GitHub), but neither is declared.
- No delivery-level fix would be needed for `FAQPage` or `BreadcrumbList` on their own — their
  properties are complete; their only problem is the same server-invisibility described above.

## Mismatches with visible content

None found — the `FAQPage` Q&A pairs match the visible FAQ section verbatim, and the
`Organization` name matches the visible company name.

## Recommended JSON-LD changes

Emit the blocks in the initial server response (in Next.js App Router, return them from the
route's `generateMetadata`/server component so they are part of the streamed HTML rather than a
client-hydrated payload), and complete the `Organization` entity while you are there:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Northwind Labs",
  "url": "https://northwind-labs.example",
  "logo": "https://northwind-labs.example/logo.svg",
  "sameAs": [
    "https://www.linkedin.com/company/northwind-labs",
    "https://github.com/northwind-labs"
  ]
}
```

## Verification tools or commands

Re-run both passes after the change; the counts must match.

```bash
curl -s "https://northwind-labs.example" | grep -oiE '<script[^>]+application/ld\+json[^>]*>' | wc -l
chrome --headless=new --disable-gpu --dump-dom "https://northwind-labs.example" \
  | grep -oiE '<script[^>]+application/ld\+json[^>]*>' | wc -l
```

Validate the emitted blocks at https://validator.schema.org, and check rich-result eligibility
separately at https://search.google.com/test/rich-results.

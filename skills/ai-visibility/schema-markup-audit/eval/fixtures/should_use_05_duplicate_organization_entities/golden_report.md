## Existing schema types found

- Three separate `Organization` blocks: one on the homepage, one on the about page, one on the contact page.

## Missing or weak schema

- `sameAs` is absent on all three blocks even though the footer links to the company's Twitter and LinkedIn profiles on every page.
- `contactPoint` is absent even though a support phone number is visible in the footer.

## Mismatches with visible content

- The three `Organization` blocks use three different `name` values ("Example Corp", "Example Corp Inc.", "Example Corporation") and three different `url` values for what should be one entity — `references/checks.md` requires one canonical `Organization` entity site-wide, not one per page.

## Recommended JSON-LD changes

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Corp",
  "url": "https://example-corp.com/",
  "sameAs": [
    "https://twitter.com/examplecorp",
    "https://linkedin.com/company/examplecorp"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "(555) 010-3000",
    "contactType": "customer support"
  }
}
```

Emit this single block on every page, pointed at the same canonical `url`, instead of three page-specific variants.

## Verification tools or commands

```bash
curl -s "https://example-corp.com/" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
```

Validate at https://validator.schema.org; check rich-result eligibility separately at https://search.google.com/test/rich-results.

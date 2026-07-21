## Existing schema types found

- `FAQPage` with one `Question`/`acceptedAnswer` pair at `https://help.example.com/shipping-faq`.

## Missing or weak schema

- The second visible Q&A pair ("Do you ship internationally?") has no corresponding `Question`/`acceptedAnswer` entry in the schema at all.

## Mismatches with visible content

- The schema's `acceptedAnswer.text` for the shipping-time question says "3-5 business days", but the visible page answer says "5-7 business days" — the schema does not match verbatim, which `references/checks.md` requires for FAQPage.

## Recommended JSON-LD changes

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does standard shipping take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Standard shipping takes 5-7 business days."
      }
    },
    {
      "@type": "Question",
      "name": "Do you ship internationally?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, we ship to over 40 countries."
      }
    }
  ]
}
```

## Verification tools or commands

```bash
curl -s "https://help.example.com/shipping-faq" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
```

Validate at https://validator.schema.org; check rich-result eligibility separately at https://search.google.com/test/rich-results — a mismatched FAQ answer can still validate structurally while misleading answer engines and users.

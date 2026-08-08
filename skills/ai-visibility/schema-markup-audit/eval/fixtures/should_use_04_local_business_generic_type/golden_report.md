## Existing schema types found

- `LocalBusiness` with `name` and a partial `address` at `https://example-bistro.com/`.

## Missing or weak schema

- The type is the generic `LocalBusiness` even though the page is clearly a restaurant — `references/checks.md` requires typing as specific as truthful (`Restaurant`, not `LocalBusiness`).
- `address` is missing `addressRegion`, `postalCode`, and `addressCountry`.
- `telephone` is absent even though the page shows a phone number.
- `openingHoursSpecification` is absent even though the page states hours (Tue-Sun 11am-9pm).
- `geo` is absent.

## Mismatches with visible content

None found — the properties that are present match the visible page content.

## Recommended JSON-LD changes

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Example Bistro",
  "telephone": "(555) 010-2222",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "44 Elm Street",
    "addressLocality": "Portland"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "opens": "11:00",
    "closes": "21:00"
  }
}
```

## Verification tools or commands

```bash
curl -s "https://example-bistro.com/" | grep -oiE 'itemtype="[^"]*"' | sort -u
```

Validate at https://validator.schema.org; check rich-result eligibility separately at https://search.google.com/test/rich-results.

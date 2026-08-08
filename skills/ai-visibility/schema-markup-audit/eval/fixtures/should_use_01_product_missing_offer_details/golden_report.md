## Existing schema types found

- `Product` with a nested `Offer` (`name`, `image`, `description`, `offers.price`) at `https://shop.example.com/products/trail-runner-boot`.

## Missing or weak schema

- `offers.priceCurrency` is absent — the price "149.00" has no currency attached.
- `offers.availability` is absent even though the page states the item is in stock.
- `brand` is absent even though the page names "Summit Gear".
- Neither `sku` nor `gtin` is present even though the page gives a model number (SG-4471) that could populate `sku`.

## Mismatches with visible content

None found — the properties that are present (`name`, `image`, `description`, `price`) match the visible page content.

## Recommended JSON-LD changes

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Trail Runner Boot",
  "image": "https://shop.example.com/img/trail-runner-boot.jpg",
  "description": "Waterproof hiking boot for rugged trails.",
  "brand": "Summit Gear",
  "sku": "SG-4471",
  "offers": {
    "@type": "Offer",
    "price": "149.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

## Verification tools or commands

```bash
curl -s "https://shop.example.com/products/trail-runner-boot" | grep -oE '<script type="application/ld\+json">[^<]*' | sed 's/^<script[^>]*>//' | python3 -m json.tool
```

Then validate at https://validator.schema.org and check rich-result eligibility separately at https://search.google.com/test/rich-results — passing the generic validator does not by itself guarantee rich-result eligibility.

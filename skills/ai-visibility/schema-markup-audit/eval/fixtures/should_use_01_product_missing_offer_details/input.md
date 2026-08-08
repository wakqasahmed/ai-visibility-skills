Audit the structured data on our product page `https://shop.example.com/products/trail-runner-boot`.

Visible page content: "Trail Runner Boot" hiking boot, $149.00 USD, in stock, brand "Summit Gear", model number SG-4471.

Existing JSON-LD found on the page:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Trail Runner Boot",
  "image": "https://shop.example.com/img/trail-runner-boot.jpg",
  "description": "Waterproof hiking boot for rugged trails.",
  "offers": {
    "@type": "Offer",
    "price": "149.00"
  }
}
```

What's missing or wrong, and what should we add?

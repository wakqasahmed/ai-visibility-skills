Audit the image schema on our product page `https://shop.example.com/products/ceramic-mug`.

Visible page content includes a photo credit line under the main image: "Photo: Jordan Lee".

Existing JSON-LD found on the page:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Ceramic Mug",
  "image": "https://shop.example.com/img/ceramic-mug.jpg",
  "offers": {
    "@type": "Offer",
    "price": "18.00",
    "priceCurrency": "USD"
  }
}
```

Is the image schema complete?

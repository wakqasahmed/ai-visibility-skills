Audit the structured data on our support page `https://help.example.com/shipping-faq`.

Visible on-page Q&A:
- Q: "How long does standard shipping take?" A: "Standard shipping takes 5-7 business days."
- Q: "Do you ship internationally?" A: "Yes, we ship to over 40 countries."

Existing JSON-LD found on the page:

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
        "text": "Standard shipping takes 3-5 business days."
      }
    }
  ]
}
```

Does this schema match the page? What should we fix?

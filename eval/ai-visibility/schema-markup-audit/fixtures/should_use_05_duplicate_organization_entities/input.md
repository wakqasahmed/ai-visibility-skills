Audit the structured data across our site `https://example-corp.com/`. We found that the homepage, about page, and contact page each carry their own `Organization` JSON-LD block:

Homepage:
```json
{"@context": "https://schema.org", "@type": "Organization", "name": "Example Corp", "url": "https://example-corp.com/"}
```

About page:
```json
{"@context": "https://schema.org", "@type": "Organization", "name": "Example Corp Inc.", "url": "https://example-corp.com/about"}
```

Contact page:
```json
{"@context": "https://schema.org", "@type": "Organization", "name": "Example Corporation", "url": "https://example-corp.com/contact"}
```

The company's social profiles are linked in the footer on every page: twitter.com/examplecorp and linkedin.com/company/examplecorp. There's a support phone line, (555) 010-3000, listed in the footer too.

What's wrong with this, and what should we do?

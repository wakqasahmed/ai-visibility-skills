We want ChatGPT and Perplexity to be able to answer questions about our product using our FAQ page. Site: https://homebrewkits.example

Representative page (`https://homebrewkits.example/faq`), fetched normally:

```html
<section id="faq">
  <h2>FAQ</h2>
  <h3>Is this kit good for beginners?</h3>
  <p>Yes.</p>
  <h3>How long does fermentation take?</h3>
  <p>About a week.</p>
  <h3>Do you ship internationally?</h3>
  <p>Yes.</p>
</section>
```

Discoverability and structured data both check out fine (robots.txt allows all major AI crawlers, sitemap.xml returns 200, JSON-LD Product schema is present on the product pages).

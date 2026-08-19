Check whether `https://shop.example.com/products/trail-runner-boot-legacy` is an orphan page.

`sitemap.xml` contains:
```
<loc>https://shop.example.com/products/trail-runner-boot-legacy</loc>
```

Internal-link crawl output (homepage + top 5 category pages, hrefs extracted and normalized):
```
https://shop.example.com/
https://shop.example.com/collections/mens-running-shoes
https://shop.example.com/collections/womens-running-shoes
https://shop.example.com/products/trail-runner-boot
https://shop.example.com/products/road-runner-sneaker
https://shop.example.com/about
https://shop.example.com/contact
```

`trail-runner-boot-legacy` does not appear anywhere in that link set.

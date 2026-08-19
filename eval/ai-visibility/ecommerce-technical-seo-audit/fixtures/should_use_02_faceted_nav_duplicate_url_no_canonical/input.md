Check our faceted navigation for duplicate-URL issues. Sampled category:
`https://shop.example.com/collections/mens-running-shoes`

Fetch results:

```
GET https://shop.example.com/collections/mens-running-shoes
200
<link rel="canonical" href="https://shop.example.com/collections/mens-running-shoes">

GET https://shop.example.com/collections/mens-running-shoes?color=blue
200
(no <link rel="canonical"> tag in the response)
(no <meta name="robots"> tag in the response)
```

robots.txt has no rule for `color=`.

What's the finding?

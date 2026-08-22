Run the commerce protocol discovery probes on `https://basicshop.example.com`. It's a small
ecommerce store — `Product`/`Offer` JSON-LD on every product page, "Add to Cart" buttons
throughout.

```
$ curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/.well-known/ucp"
404
$ curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/.well-known/agent-card.json"
404
$ curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/products.json"
404
$ curl -s -o /dev/null -w "%{http_code}\n" "https://basicshop.example.com/catalog.json"
404
$ curl -s "https://basicshop.example.com/robots.txt" | grep -iE "feed|sitemap"
Sitemap: https://basicshop.example.com/sitemap.xml
```

No MCP endpoint mentioned anywhere. What did the discovery pass find?

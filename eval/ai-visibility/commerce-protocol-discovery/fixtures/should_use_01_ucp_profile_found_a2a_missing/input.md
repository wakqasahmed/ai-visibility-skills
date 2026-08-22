Check `https://shop.example.com` for agentic-commerce discovery surface. It's a Shopify store —
`Product`/`Offer` JSON-LD is present on product pages and there's an "Add to Cart" button.

```
$ curl -s -o /dev/null -w "%{http_code}\n" "https://shop.example.com/.well-known/ucp"
200
$ curl -s -o /dev/null -w "%{http_code}\n" "https://shop.example.com/.well-known/agent-card.json"
404
$ curl -s -o /dev/null -w "%{http_code}\n" "https://shop.example.com/products.json"
200
```

No MCP endpoint is mentioned anywhere on the site or in its docs. What's discoverable here?

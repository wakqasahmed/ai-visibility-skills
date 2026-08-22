Discovery-only pass on `https://store.example.net`, a marketplace with `Product` schema and a
`/cart` checkout flow.

```
$ curl -s -o /dev/null -w "%{http_code}\n" "https://store.example.net/products.json"
200
$ curl -s "https://store.example.net/products.json" | python3 -m json.tool | head -5
{
  "products": [
    {"id": 991, "title": "Trail Runner Backpack 22L", "variants": [{"price": "89.00"}]}
  ]
```

We checked the live product page for the same item and it currently shows $109.00 and "in
stock." `.well-known/ucp` and `.well-known/agent-card.json` both 404. No MCP endpoint claimed.

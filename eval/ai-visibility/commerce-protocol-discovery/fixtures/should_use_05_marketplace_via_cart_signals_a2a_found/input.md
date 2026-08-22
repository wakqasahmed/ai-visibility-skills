`https://marketplace.example.io` doesn't use Schema.org `Product` markup at all, but it has a
`/checkout` flow and "Add to cart" buttons on every listing, and a `/cart` page. Run the
discovery probes.

```
$ curl -s -o /dev/null -w "%{http_code}\n" "https://marketplace.example.io/.well-known/agent-card.json"
200
$ curl -s "https://marketplace.example.io/.well-known/agent-card.json" | python3 -m json.tool | head -5
{
  "name": "marketplace-example-agent",
  "version": "1.0.0"
$ curl -s -o /dev/null -w "%{http_code}\n" "https://marketplace.example.io/.well-known/ucp"
404
$ curl -s -o /dev/null -w "%{http_code}\n" "https://marketplace.example.io/products.json"
404
```

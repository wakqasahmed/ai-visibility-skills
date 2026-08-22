`https://tools.example.org` sells subscriptions and merchandise (`Product` JSON-LD on the
merch pages, "Add to cart" present). Their docs mention a remote MCP server at
`https://mcp.tools.example.org/mcp` for order-status lookups. We hit it unauthenticated:

```
$ curl -sI "https://mcp.tools.example.org/mcp"
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://mcp.tools.example.org/.well-known/oauth-protected-resource"
```

`.well-known/ucp` → 404. `.well-known/agent-card.json` → 404. No `/products.json` or
`/catalog.json` found; robots.txt has no feed reference.

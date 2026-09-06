# Commerce protocol discovery check commands

Replace `$SITE` with the storefront origin. These four probes are mechanical and
non-scored — record only the endpoint probed and the observed status code/result, never a
`ready`/`partial`/`missing`/`verified` label.

## 1. UCP business profile

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/ucp"
```

Probe `/.well-known/ucp` only when UCP is relevant. Its specification defines this discovery
location. [UCP-SPEC-01]

## 2. A2A Agent Card

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/agent-card.json"
```

Probe `/.well-known/agent-card.json` only when the site claims to host an A2A server. Its
specification defines this discovery location. [A2A-SPEC-01]

## 3. MCP: protected endpoint challenge

For a protected remote MCP endpoint, inspect its `401` `WWW-Authenticate` challenge and the
referenced OAuth Protected Resource Metadata rather than guessing a site-root manifest.
[MCP-AUTH-01]

Only run this probe when an MCP endpoint is claimed or discoverable — do not invent a
site-root manifest path to guess against.

## 4. Catalog feeds

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/products.json"
curl -s "$SITE/products.json" | python3 -m json.tool | head -40
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/catalog.json"
curl -s "$SITE/robots.txt" | grep -iE "feed|sitemap"
curl -s "$SITE/sitemap.xml" | grep -iE "feed|google-shopping|catalog"
```

A publicly hosted machine-readable catalog is a strong agent-discovery signal, but no current
protocol requires merchants to publish one at a well-known path: ACP feeds are submitted to the
agent platform (file upload or feed API) rather than served from the merchant's domain, so an
absent public feed is a weak negative, never a hard fail. [ACP-SPEC-01]

Interpret what you find, in order:

1. Platform-native JSON listings such as `/products.json` (observed Shopify convention) — pass
   when it returns a parseable product collection; record the item count as evidence.
2. Google Merchant Center feeds (RSS 2.0 or Atom with the `g:` namespace, or a delimited text
   feed) — often referenced from a CMS plugin or supplied by the merchant; validate against the
   Merchant Center product data specification. [GOOGLE-MERCHANT-FEED-01]
3. Community-plugin conventions such as `/catalog.json` or `/sitemap-ai.xml` — useful when
   present, but treat them as observed plugin output, not standards; never fail a store for
   missing them.
4. When the merchant claims ACP support, validate their feed artifacts against the dated ACP
   feed schema version they pin to, not against HEAD. [ACP-SPEC-01]

For any feed found, sample one item and compare its price and availability against the live
product page; a stale feed misleads agents more than no feed. Flag variable products whose feed
entries collapse to a `$0` or base-price-only offer.

## [EXPERIMENTAL] Third-Party Agent Readiness Attestation (isitagentready.com)

This probe checks an emerging third-party benchmark (`isitagentready.com`) for public production
domains where external network requests and third-party benchmark checks are permitted. It is
strictly marked `[EXPERIMENTAL]` in reports, is informational only, and never reduces the core
score:

```bash
# Privacy Guard: Only run against public domains, never internal/staging/private-network URLs
if [[ "$SITE" =~ ^https?://(localhost|127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|\[?(::1|[fF][cCdD][0-9a-fA-F]{0,2}:)|.*\.internal|.*\.local|.*\.staging) ]]; then
  echo "Private/staging target detected — skipping external third-party scan for privacy."
else
  curl -s -m 10 -X POST "https://isitagentready.com/api/scan" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c 'import json,sys; print(json.dumps({"url": sys.argv[1]}))' "$SITE")" \
    | python3 -m json.tool || echo "External attestation scan unavailable."
fi
```

When reporting these findings, always include an `[EXPERIMENTAL]` label and note that adoption is
optional and draft-stage — record only the endpoint probed and the observed result, never a
scored assessment, and never let it corroborate or substitute for a `[Measured]` first-party
finding.

## Evidence discipline

Record every probe as: endpoint probed, command run, and observed HTTP status/result — never
as a scored assessment. This skill reports discoverability only; it does not judge whether an
implementation is correct, complete, or safe.

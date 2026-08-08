## Claims and canonical URLs

### Claim: 2-business-day US shipping
- URL: https://www.acmewidgets.example/shipping-policy
- Verdict: blocker
- Evidence: `curl -s -o /dev/null -w "%{http_code} %{url_effective}" .../shipping-policy` returns a 301 -> 302 -> 200 redirect chain ending at `/help/shipping`; the requested page is not the URL AI systems would land on.

## Citation blockers

- 2-business-day US shipping: 3-hop redirect chain (301 -> 301 -> 302 -> 200). The claim has no stable, self-referential canonical URL — an AI system citing `/shipping-policy` today may resolve to a different final page tomorrow if the chain changes.

## Trust and freshness gaps

- None assessed yet; resolve the canonical URL first so trust signals can be checked on the actual destination page.

## Recommended page fixes

- Collapse the redirect chain to a single 301 hop (or none) from `/shipping-policy` directly to the final destination, or move the canonical content to `/shipping-policy` itself.
- Add a self-referential `<link rel="canonical">` on the final destination page.

## Claims to remove or substantiate

- 2-business-day US shipping: do not mark citable until the canonical URL resolves in one hop (or zero) to a stable, indexable page.

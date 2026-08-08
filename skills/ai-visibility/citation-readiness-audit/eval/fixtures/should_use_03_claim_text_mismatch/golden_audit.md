## Claims and canonical URLs

### Claim: $12/user/month starting price
- URL: https://www.driftcloud.example/pricing
- Verdict: needs_substantiation
- Evidence: page returns 200, but grepping the server-rendered, tag-stripped HTML for "$12/user/month" returns no output — the claim is rendered client-side only (`<div id="pricing-app"></div>` placeholder in the raw response) and is not actually present in what a non-executing crawler fetches.

## Citation blockers

- $12/user/month starting price: not a hard block (page is indexable), but the claim text is absent from server-rendered content, so most AI crawlers will not see it.

## Trust and freshness gaps

- Cannot assess author/date/org signals for a claim that isn't in the fetched HTML in the first place.

## Recommended page fixes

- Server-render (or statically pre-render) the pricing figures so the exact claim text is present in the initial HTML response, not only in the client-side bundle.

## Claims to remove or substantiate

- $12/user/month starting price: do not mark citable until the claim text is verifiable in server-rendered content matching the on-page text.

## Claims and canonical URLs

### Claim: 99.9% uptime SLA on enterprise plan
- URL: https://www.brightleaf.example/enterprise/sla
- Verdict: blocker
- Evidence: page returns 200 and the claim text "99.9% uptime" appears in server-rendered content, but `<meta name="robots" content="noindex, follow">` is present — noindex means AI crawlers and search-adjacent indexes are directed not to index the page.

## Citation blockers

- 99.9% uptime SLA on enterprise plan: `noindex` robots meta tag on the only page carrying this claim.

## Trust and freshness gaps

- Not assessed until the noindex directive is resolved; an AI system is unlikely to have indexed this page's author/date/org signals either.

## Recommended page fixes

- Remove `noindex` from `/enterprise/sla` if this page is meant to be publicly citable, or move the SLA claim to a page that is already indexable.

## Claims to remove or substantiate

- 99.9% uptime SLA on enterprise plan: do not mark citable while the page carries a noindex directive.

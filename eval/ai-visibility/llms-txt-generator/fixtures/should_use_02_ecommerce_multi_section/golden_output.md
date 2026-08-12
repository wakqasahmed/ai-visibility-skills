## Proposed llms.txt

```markdown
# Brightleaf

Brightleaf sells sustainable home goods, including kitchen and bedding collections.

## Products

- [Kitchen Collection](https://brightleaf.store/collections/kitchen): Sustainable kitchenware and tools.
- [Bedding Collection](https://brightleaf.store/collections/bedding): Organic and sustainably sourced bedding.

## Policies

- [Shipping Policy](https://brightleaf.store/shipping-policy): Shipping times, carriers, and costs.
- [Returns Policy](https://brightleaf.store/returns-policy): Return window and refund process.

## Support

- [Support](https://brightleaf.store/support): Customer help center.
- [Contact](https://brightleaf.store/contact): Ways to reach the team directly.

## Company

- [About](https://brightleaf.store/about): Brightleaf's mission and sourcing practices.
```

## Placement path

`/llms.txt` at the site root (`https://brightleaf.store/llms.txt`). No existing file found (404) — new placement.

## Source URLs used

All 8 URLs from `sitemap.xml`: homepage, two collection pages, shipping and returns policies, support, contact, and about — each confirmed HTTP 200.

## Missing recommended URLs or pages

None identified — the sitemap covers products, policies, support, and company info.

## Verification steps

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://brightleaf.store/llms.txt"
# expect: 200 after publishing
curl -s "https://brightleaf.store/llms.txt" | grep -c '^## '
# expect: 4
```

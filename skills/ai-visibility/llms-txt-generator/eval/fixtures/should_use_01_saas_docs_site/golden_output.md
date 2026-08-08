## Proposed llms.txt

```markdown
# AcmeFlow

AcmeFlow automates repetitive team workflows with no-code triggers and integrations.

## Docs

- [Documentation](https://acmeflow.dev/docs): Product docs and guides.
- [Quickstart](https://acmeflow.dev/docs/quickstart): Get a first workflow running in minutes.

## Product

- [Integrations](https://acmeflow.dev/integrations): Supported third-party connections.
- [Pricing](https://acmeflow.dev/pricing): Plans and pricing tiers.

## Support & Policies

- [Support](https://acmeflow.dev/support): Help center and contact options.
- [Privacy Policy](https://acmeflow.dev/privacy): How AcmeFlow handles user data.
- [Terms of Service](https://acmeflow.dev/terms): Terms governing use of AcmeFlow.
```

## Placement path

`/llms.txt` at the site root (`https://acmeflow.dev/llms.txt`). No existing file was found (404), so this is a new placement, not a replacement.

## Source URLs used

All 8 URLs come from `sitemap.xml`, spot-checked individually and confirmed to return HTTP 200: the homepage, `/docs`, `/docs/quickstart`, `/pricing`, `/integrations`, `/support`, `/privacy`, `/terms`.

## Missing recommended URLs or pages

None identified from the crawl — the sitemap already covers docs, pricing, integrations, support, and policy pages.

## Verification steps

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://acmeflow.dev/llms.txt"
# expect: 200 after publishing
curl -sI "https://acmeflow.dev/llms.txt" | grep -i content-type
# expect: text/plain or text/markdown, not text/html
curl -s "https://acmeflow.dev/llms.txt" | grep -c '^## '
# expect: 3
```

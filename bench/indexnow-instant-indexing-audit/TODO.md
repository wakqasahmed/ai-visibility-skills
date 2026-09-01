# Benchmark TODO: indexnow-instant-indexing-audit

- [ ] Collect test dataset of sites with known IndexNow states: root key file, non-root `keyLocation`, edge-delegated Cloudflare Crawler Hints, and no implementation.
- [ ] Measure `403` vs `422` classification accuracy — key-validation failure versus `keyLocation` path-scope violation is the audit's core diagnostic and the easiest to conflate.
- [ ] Benchmark CMS push-trigger detection across WordPress, Next.js, Shopify, and CI-driven pipelines.
- [ ] Verify the audit never performs a live submission without explicit operator authorization.

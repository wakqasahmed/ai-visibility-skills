# Benchmark TODO: semantic-entity-topical-map-audit

- [ ] Collect a test dataset of sites with known-ambiguous brand names, split by whether a Wikidata item exists for the organization.
- [ ] Measure JSON-LD extraction accuracy against minified, pretty-printed, and `@graph`-wrapped markup, since the pretty-printed-only grep this skill replaced produced false "schema missing" findings.
- [ ] Measure `sameAs` target-resolution accuracy: how often a declared Wikidata item actually describes the declaring organization.
- [ ] Benchmark orphan-subtopic detection (sitemap URL set vs. pillar outbound links) against a full-crawl ground truth to quantify the sampling error of the sitemap-comparison method.
- [ ] Check classification stability: does the same site get the same `AMBIGUOUS`/`PARTIALLY_GROUNDED`/`FULLY_RECONCILED` label across repeated runs?

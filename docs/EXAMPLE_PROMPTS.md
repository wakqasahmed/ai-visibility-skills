# Example prompts

**These are illustrative usage examples, not verified test runs.** Nobody has executed
these prompts against a live website and recorded the real output yet — this file shows
what you'd type and what kind of report structure the invoked skill's own `SKILL.md`
promises, grounded in each skill's `## Output` section. It does not claim any of these
runs actually happened. If you run one of these for real and want to contribute the actual
output, open a PR that replaces the relevant "expected output shape" block with the real
result and a link to the evidence (e.g. a saved run log or PR that used it).

This distinction matters because this pack's own [shared guardrails](../skills/ai-visibility/references/guardrails.md)
say: don't present an inference as an observed result. Labeling these as tested would
violate that principle.

---

## Example 1 — general AI visibility check

**Skill invoked:** [`ai-visibility-audit`](../skills/ai-visibility/ai-visibility-audit/SKILL.md)

**Prompt:**

> "Can ChatGPT, Perplexity, and Google AI Overviews find and cite our site,
> `https://example-store.com`? Run an AI visibility audit and tell me what's blocking us."

**Expected output shape** (per the skill's `## Output` section):

- Overall score — ready, partially ready, or blocked
- Top 5 blockers
- Evidence with URLs (observed page evidence, not inferred)
- Quick wins
- Implementation tickets or next actions

---

## Example 2 — crawler access review

**Skill invoked:** [`robots-ai-crawler-audit`](../skills/ai-visibility/robots-ai-crawler-audit/SKILL.md)

**Prompt:**

> "Check `robots.txt` and any meta-robots/header rules on `https://example-store.com` —
> are we accidentally blocking GPTBot, ClaudeBot, or PerplexityBot from our product and
> docs pages?"

**Expected output shape:**

- Current crawler policy summary
- Blocked high-value paths
- AI crawler implications
- Recommended `robots.txt` changes
- Verification commands

---

## Example 3 — llms.txt drafting

**Skill invoked:** [`llms-txt-generator`](../skills/ai-visibility/llms-txt-generator/SKILL.md)

**Prompt:**

> "Draft an `llms.txt` for `https://example-store.com` using our sitemap, product pages,
> and support docs, so AI agents know which pages matter most."

**Expected output shape:**

- Proposed `llms.txt` content
- Placement path (`/llms.txt`)
- Source URLs used
- Missing recommended URLs or pages
- Verification steps

---

## Example 4 — audit findings into a remediation plan

**Skills invoked:** [`schema-markup-audit`](../skills/ai-visibility/schema-markup-audit/SKILL.md)
then [`ai-search-remediation-plan`](../skills/ai-visibility/ai-search-remediation-plan/SKILL.md)

**Prompt:**

> "Audit our schema.org JSON-LD on `https://example-store.com/products/*` for AI search
> and rich results, then turn whatever you find into a prioritized implementation
> checklist I can hand to engineering."

**Expected output shape:**

From `schema-markup-audit`:
- Existing schema types found
- Missing or weak schema
- Mismatches with visible content
- Recommended JSON-LD changes
- Verification tools or commands

Fed into `ai-search-remediation-plan`, which turns those findings into:
- Priority roadmap
- Issue-sized tasks
- Acceptance criteria
- Verification commands or manual checks
- Owner decisions and blockers

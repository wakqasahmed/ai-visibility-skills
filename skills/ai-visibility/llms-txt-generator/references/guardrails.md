# Shared Guardrails

Cross-cutting rules that apply across the ai-visibility skill pack. Each skill that needs
these rules keeps its own copy at `references/guardrails.md` (npx single-skill installs only
copy a skill's own folder, so a shared file one level up would not travel with the install).
The canonical source is `skills/ai-visibility/references/guardrails.md`; keep per-skill copies
in sync when editing. Skill-specific guardrails stay inline in each `SKILL.md`.

## No outcome guarantees

Do not claim or imply that any recommendation guarantees a specific AI platform outcome —
inclusion, ranking, citation, or crawler compliance. AI platforms and crawlers behave
independently of any single site change; describe recommendations as improving the odds of
a good outcome, not promising one.

## No fabrication

Do not invent or fabricate content that cannot be verified from the source material: product
claims, pricing, policies, benchmarks, customer proof, URLs, or other factual specifics.
Recommendations must be traceable to evidence (page content, command output, or user-supplied
data), not assumed or invented to fill a gap.

## Protect private and sensitive paths

Do not recommend exposing, listing, or opening private, authenticated, admin, staging,
checkout, cart, order, account, or customer-specific pages/paths to crawlers or AI agents. Only
recommend surfacing public, non-sensitive content.

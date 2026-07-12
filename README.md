# AI Visibility Skills [![skills.sh](https://skills.sh/b/wakqasahmed/ai-visibility-skills)](https://skills.sh/wakqasahmed/ai-visibility-skills)

Skills for auditing whether ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews, and other AI agents can discover, understand, cite, and recommend a website.

## Install

```bash
npx skills@latest add wakqasahmed/ai-visibility-skills
```

## Ask Your Agent

```text
Audit https://example.com for ChatGPT, Claude, Perplexity, Google AI Overviews, llms.txt, schema, crawler access, sitemap coverage, and citation readiness.
```

```text
Draft an llms.txt for this site and tell me which pages are missing before I publish it.
```

```text
Turn these AI visibility audit findings into prioritized implementation tickets.
```

## Skills

- `ai-visibility-audit`: full website audit for AI search and answer engines.
- `llms-txt-generator`: draft or review `/llms.txt`.
- `robots-ai-crawler-audit`: check robots.txt, meta robots, headers, and AI bot access.
- `schema-markup-audit`: review JSON-LD and schema.org markup.
- `sitemap-discovery-audit`: check sitemap coverage, canonical URLs, redirects, and indexable pages.
- `answer-engine-content-audit`: find content gaps that block AI answers and recommendations.
- `citation-readiness-audit`: check whether claims and policies have stable citeable URLs.
- `ai-search-remediation-plan`: turn findings into prioritized tasks.

## Install Related Packs

```bash
npx skills@latest add wakqasahmed/agentic-commerce-skills
npx skills@latest add wakqasahmed/ai-engineering-workflow-skills
npx skills@latest add wakqasahmed/skills
```

## Security

See [SECURITY.md](SECURITY.md) for what these skills are (instruction files, not
executable code), which skills document outbound network checks, and how to report a
security concern.
## Testing

`ai-visibility-audit` has an offline behavioral eval fixture that checks the skill
actually ranks blockers, cites evidence, and delegates to the focused skills instead
of redoing their work inline — no live network calls or LLM in the loop:

```bash
python3 skills/ai-visibility/ai-visibility-audit/eval/run_eval.py
```

See `skills/ai-visibility/ai-visibility-audit/eval/README.md` for what it checks and
how to add new fixture cases.

## Marketplace And Discovery

- Public install command: `npx skills@latest add wakqasahmed/ai-visibility-skills`
- skills.sh page: `https://skills.sh/wakqasahmed/ai-visibility-skills`
- GitHub repo: `https://github.com/wakqasahmed/ai-visibility-skills`

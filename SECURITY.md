# Security Policy

## What this repository is

This repository contains **Agent Skills**: Markdown instruction files (`SKILL.md` and
`references/*.md`) that an AI agent reads and follows. They are prompts, not executable
code. Installing a skill does not run a script on your machine by itself — the risk
surface is in what an agent is *instructed* to do when it follows the skill, not in a
build or install step.

A few skills go further and document shell commands (mainly `curl`) that an agent may
run against a **user-supplied URL** to gather evidence (e.g. fetching `robots.txt` or
page HTML). Anyone installing these skills should be aware their agent may make outbound
HTTP requests to sites they name during an audit:

- `skills/ai-visibility/ai-visibility-audit/references/checks.md` — documents `curl`
  commands against `$SITE` / `$URL` for robots.txt, redirects, headers, and page markup.
- `skills/ai-visibility/schema-markup-audit/references/checks.md` — documents `curl`
  commands against `$URL` to extract JSON-LD/microdata.

These commands only target the site the user asked to audit; no skill in this repo
instructs fetching arbitrary or attacker-supplied URLs, exfiltrating data, or running
commands unrelated to the stated audit. If you find a skill that does, please report it
using the process below.

## Scope

In scope:
- A `SKILL.md` or reference file that instructs an agent to run destructive, obfuscated,
  or unrelated-to-purpose commands.
- A `SKILL.md` or reference file that instructs an agent to exfiltrate data, credentials,
  or file contents to a third party.
- Prompt-injection-style content designed to make an agent ignore its operator's
  instructions or safety guidance.
- Malicious links, typosquatted install commands, or supply-chain issues in this repo
  or its install scripts (`scripts/`).

Out of scope:
- The behavior of the AI agent or client itself once it is following a skill (report
  those to the agent/client vendor).
- The security posture of third-party sites that a skill's checks are run against.
- General suggestions or feature requests — open a regular GitHub issue for those.

## Reporting a Concern

Please report security concerns privately rather than opening a public issue:

1. Email the maintainer at wakqasahmed@gmail.com with a description of the concern,
   the affected file(s), and, if applicable, the specific instruction text you consider
   risky.
2. If email is not available to you, open a GitHub issue at
   https://github.com/wakqasahmed/ai-visibility-skills/issues and mark it clearly with
   `[SECURITY]` in the title so it can be triaged before other traffic gets to it. Avoid
   including exploit details in the public issue body if the concern is sensitive —
   note that a private report is available and the maintainer will follow up.

We aim to acknowledge reports within a few business days and will credit reporters in
the fix commit unless you ask to stay anonymous.

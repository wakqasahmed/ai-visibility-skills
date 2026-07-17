# Robots and AI crawler check commands

Replace `$SITE` with the site origin and `$URL` with a representative high-value page.

## Fetch and read robots.txt

```bash
curl -s "$SITE/robots.txt"
curl -sI "$SITE/robots.txt" | head -1
curl -s "$SITE/robots.txt" | grep -i "^sitemap"
curl -s "$SITE/robots.txt" | grep -iE "^(user-agent|disallow|allow|crawl-delay)"
```

## Per-bot rule extraction

```bash
curl -s "$SITE/robots.txt" | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
```

## Known AI crawler user-agents to check for explicit allow/deny blocks

```bash
for ua in GPTBot ChatGPT-User OAI-SearchBot ClaudeBot Claude-Web anthropic-ai PerplexityBot Google-Extended Applebot-Extended Bytespider CCBot Amazonbot; do
  printf "%-20s " "$ua"
  curl -s "$SITE/robots.txt" | grep -qi "^user-agent:\s*$ua" && echo "explicit block found in robots.txt" || echo "no explicit rule"
done
```

## Live fetch as each bot (edge/WAF blocks won't show in robots.txt)

```bash
for ua in GPTBot ClaudeBot PerplexityBot Google-Extended CCBot Amazonbot; do
  printf "%-16s " "$ua"
  curl -s -o /dev/null -w "%{http_code}\n" -A "$ua" "$URL"
done
```

If a bot gets a different status code (403, 429, redirect) than a default user-agent, that's an edge block invisible to robots.txt inspection alone — flag as critical.

## Page-level directives

```bash
curl -s "$URL" | grep -oiE '<meta[^>]+robots[^>]+>'
curl -sI "$URL" | grep -i "x-robots-tag"
curl -s "$URL" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
```

## Evidence discipline

Record each finding as: URL or bot checked, command run, observed output, and whether it blocks or helps AI crawler access. Do not infer a block without an observed status code or explicit robots.txt rule.

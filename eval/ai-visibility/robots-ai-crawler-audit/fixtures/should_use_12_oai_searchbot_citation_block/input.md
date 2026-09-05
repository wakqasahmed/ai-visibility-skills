# Request

We allow OpenAI's training crawler, but ChatGPT search still does not cite our
public pages. Check whether our crawler policy explains the problem.

## robots.txt (fetched from https://example.com/robots.txt)

```
User-agent: *
Disallow:

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Disallow: /

Sitemap: https://example.com/sitemap.xml
```

## Per-bot rule extraction

```
$ curl -s https://example.com/robots.txt | awk 'BEGIN{IGNORECASE=1} /^user-agent:/{ua=$0} /^disallow:|^allow:/{print ua" | "$0}'
User-agent: * | Disallow:
User-agent: GPTBot | Allow: /
User-agent: OAI-SearchBot | Disallow: /
```

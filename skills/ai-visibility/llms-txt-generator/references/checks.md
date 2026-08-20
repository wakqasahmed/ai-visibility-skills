# llms.txt check commands

Replace `$SITE` with the site origin.

## Check whether llms.txt already exists

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/llms.txt"
curl -s "$SITE/llms.txt"
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/llms-full.txt"
```

If `/llms.txt` returns 200, fetch and review it before drafting a replacement — do not silently overwrite an existing file's intent.

## Verify it's served as plain text, not HTML fallback

```bash
curl -sI "$SITE/llms.txt" | grep -i content-type
```

A `text/html` content-type on a 200 response usually means the server returned a catch-all page (e.g. SPA fallback or custom 404 rendered as 200), not a real file.

## Gather source material for drafting

```bash
curl -s "$SITE/robots.txt" | grep -i "^sitemap"
curl -s "$SITE/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//'
curl -s "$SITE" | grep -oE '<title>[^<]*'
curl -s "$SITE" | grep -oE '<meta name="description"[^>]*>'
```

## After drafting: validate placement and format

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/llms.txt"
curl -s "$SITE/llms.txt" | head -5
```

Confirm the file starts with an H1 and short summary (the established llms.txt convention [LLMSTXT-01]), then grouped H2 sections with markdown links, per https://llmstxt.org [LLMSTXT-01].

```bash
curl -s "$SITE/llms.txt" | grep -c '^## '
curl -s "$SITE/llms.txt" | grep -oE '\[.+\]\(https?://[^)]+\)'
```

## Spot-check that every linked URL actually resolves

```bash
for u in $(curl -s "$SITE/llms.txt" | grep -oE '\(https?://[^)]+\)' | tr -d '()'); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$u")
  echo "$code $u"
done
```

## [EXPERIMENTAL] Emerging Agent Discovery Checks (Draft Standards)

These checks evaluate emerging draft conventions surfaced by `isitagentready.com` and agent discovery working groups. They are strictly marked `[EXPERIMENTAL]` in reports and are informational — absence of these files/headers does NOT hurt standard search indexing or core `llms.txt` discovery:

1. **Markdown Content Negotiation (`Accept: text/markdown`) [MARKDOWN-NEGOTIATION-01]**:
   Check if the server serves clean Markdown representations directly via HTTP content negotiation:
   ```bash
   curl -s -i -H "Accept: text/markdown" "$SITE" | grep -i "content-type"
   curl -s -i -H "Accept: text/markdown" "$SITE" | head -20
   ```
2. **Agential Resource Discovery (`ARD`) and `auth.md` Manifests [ARD-MANIFEST-01]**:
   Check if the site publishes machine-readable agent permission manifests at standard discovery locations:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" "$SITE/auth.md"
   curl -s -o /dev/null -w "%{http_code}\n" "$SITE/.well-known/ard.json"
   ```

When reporting these findings, always include an `[EXPERIMENTAL]` label and note that adoption is optional and draft-stage.

## Evidence discipline

Record each finding as: URL checked, command run, observed output, and whether it confirms a source page's existence or a broken link in the draft. Do not include a URL in `llms.txt` that hasn't been verified to return 200.

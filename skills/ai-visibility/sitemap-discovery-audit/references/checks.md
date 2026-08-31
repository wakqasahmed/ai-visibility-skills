# Sitemap discovery check commands

Replace `$SITE` with the site origin and `$URL` with a representative sitemap URL entry.

## Find sitemap declarations

Follow what the site declares first; guess filenames last. Skipping the first two steps is how a
site that publishes its sitemap at a framework default gets reported as having none.

### 1. `Sitemap:` directives in robots.txt

```bash
curl -s "$SITE/robots.txt" | grep -iE "^[[:space:]]*sitemap:" | sed -E 's/^[[:space:]]*[Ss]itemap:[[:space:]]*//'
```

Fetch every URL this returns, including ones on a different host — a cross-host declaration is
legal, and it is also where host-mismatch problems surface (step 4).

### 2. `<link rel="sitemap">` in the homepage `<head>`

```bash
curl -s "$SITE" | grep -oiE '<link[^>]+rel="sitemap"[^>]*>'
curl -s "$SITE" | grep -oiE '<link[^>]+rel="sitemap"[^>]*>' | grep -oiE 'href="[^"]+"' | sed 's/href="//;s/"$//'
```

Match `rel="sitemap"` anywhere inside the tag — `href` and `type` frequently precede `rel`, and
an adjacent-token pattern misses those.

### 3. Probe common default paths

Only once steps 1 and 2 come up empty. Generators write different defaults, and the hyphenated
and underscored spellings are different files:

```bash
for path in \
  /sitemap.xml /sitemap_index.xml /sitemap-index.xml /sitemap/sitemap-index.xml \
  /sitemap/ /sitemap.xml.gz /sitemap-0.xml /sitemap1.xml /wp-sitemap.xml \
  /page-sitemap.xml /post-sitemap.xml; do
  printf "%-28s %s\n" "$path" "$(curl -s -o /dev/null -w '%{http_code}' "$SITE$path")"
done
```

- `/sitemap-index.xml` is `gatsby-plugin-sitemap`'s default output (it chains to `/sitemap-0.xml`).
- `/sitemap_index.xml`, `/wp-sitemap.xml`, `/page-sitemap.xml`, `/post-sitemap.xml` cover Yoast,
  core WordPress, and similar plugin layouts.
- `/sitemap.xml` covers Next.js route handlers, Hugo, Jekyll, and most hand-rolled setups.

A `200` whose `content-type` is `text/html` is an SPA fallback shell, not a sitemap:

```bash
curl -sI "$SITE/sitemap.xml" | grep -i "^content-type"
```

Report "no sitemap found" only when all three steps come up empty. When a sitemap exists but
`robots.txt` does not declare it, the missing `Sitemap:` directive is the finding — not a missing
sitemap.

### 4. Verify the sitemap's declared host actually serves the site

`<loc>` entries can advertise a host that never resolves, refuses TLS, or simply is not the
canonical host. Every entry then points crawlers at a dead address even though the sitemap
itself is well-formed and reachable.

```bash
SITEMAP_URL="$SITE/sitemap.xml"   # or whichever URL steps 1-3 actually found
curl -s "$SITEMAP_URL" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' \
  | awk -F/ '{print $1"//"$3}' | sort -u

curl -s "$SITE" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'

for host in $(curl -s "$SITEMAP_URL" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' | awk -F/ '{print $1"//"$3}' | sort -u); do
  printf "%-40s %s\n" "$host" "$(curl -s -o /dev/null -m 10 -w '%{http_code}' "$host/" || echo CONNECT-FAIL)"
done
```

A sitemap host that times out, fails TLS, or differs from the canonical host is a discovery
failure. Report it with the observed status (or connection failure) alongside the canonical host
it should have used.

## Fetch and validate sitemap structure

```bash
curl -s "$SITE/sitemap.xml" | head -c 500
curl -s "$SITE/sitemap.xml" | python3 -c "
import sys, xml.dom.minidom as m
m.parseString(sys.stdin.read())
print('well-formed XML')
"
```

## List sub-sitemaps (if this is a sitemap index) or URLs (if this is a URL set)

```bash
curl -s "$SITE/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//'
```

## Count entries and inspect lastmod freshness

```bash
curl -s "$SITE/sitemap.xml" | grep -c '<url>'
curl -s "$SITE/sitemap.xml" | grep -oE '<lastmod>[^<]+</lastmod>' | sort -u | tail -20
```

### Verify lastmod delta vs. reference audit date

```bash
# Explicitly compute chronological delta to ensure correct before/after direction.
# LASTMOD is a value pulled from the sitemap above; REF_DATE is this audit's run date.
LASTMOD="$LASTMOD" REF_DATE="$REF_DATE" python3 -c "
import os
from datetime import date
lastmod = date.fromisoformat(os.environ['LASTMOD'])
ref_date = date.fromisoformat(os.environ['REF_DATE'])
delta = (lastmod - ref_date).days
if delta < 0:
    print(f'{abs(delta)} days before reference audit ({ref_date})')
elif delta > 0:
    print(f'{delta} days after reference audit ({ref_date})')
else:
    print('identical date')
"
```

## Check representative URLs for status, redirects, and indexability

```bash
for u in $(curl -s "$SITE/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' | head -20); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$u")
  echo "$code $u"
done
```

```bash
curl -s "$URL" | grep -oiE '<meta[^>]+robots[^>]+>'
curl -s "$URL" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
```

## Broader internal-link sweep for broken/dead links

Sitemap entries are only one source of URLs. Crawl the internal links a real
visitor (or crawler) would actually follow — homepage, nav, footer, and a
sample of body links on a few representative pages — and check each one's
status, independent of whether it is listed in the sitemap:

```bash
curl -s "$SITE" | grep -oE 'href="[^"]+"' | sed 's/href="//;s/"$//' | SITE="$SITE" python3 -c '
import os, sys
from urllib.parse import urljoin, urlsplit, urlunsplit

site = os.environ["SITE"].rstrip("/")
site_parts = urlsplit(site)
for href in sys.stdin:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        continue
    link = urlsplit(urljoin(site + "/", href))
    if link.scheme != site_parts.scheme or link.netloc != site_parts.netloc:
        continue
    print(urlunsplit((link.scheme, link.netloc, link.path, link.query, "")))
' | sort -u > /tmp/internal-links.txt

while read -r u; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$u")
  echo "$code $u"
done < /tmp/internal-links.txt | grep -vE '^(2|3)[0-9]{2}'
```

Repeat the same href-extraction + status-check pass against a handful of the
site's own high-traffic internal pages (not just the homepage) to catch
broken links buried deeper than the homepage/nav, since a page can link to a
dead URL that never appears in the homepage's own `href` set.

Cross-check each broken/dead internal link against `/tmp/sitemap-links.txt`
(built in the coverage-comparison step below): a broken link that is also a
sitemap entry is a coverage-and-freshness problem; a broken link that is
never in the sitemap is still worth reporting since it degrades crawl paths
and user/agent trust even though it was never meant to be indexed via the
sitemap.

## Cross-check coverage against navigation

Manually list the site's important nav/footer links, normalize internal links to absolute
URLs, then diff against sitemap URLs to spot omissions:

```bash
curl -s "$SITE" | grep -oE 'href="[^"]+"' | sed 's/href="//;s/"$//' | SITE="$SITE" python3 -c '
import os, sys
from urllib.parse import urljoin, urlsplit, urlunsplit

site = os.environ["SITE"].rstrip("/")
site_parts = urlsplit(site)
for href in sys.stdin:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        continue
    link = urlsplit(urljoin(site + "/", href))
    if link.scheme != site_parts.scheme or link.netloc != site_parts.netloc:
        continue
    print(urlunsplit((link.scheme, link.netloc, link.path, link.query, "")))
' | sort -u > /tmp/nav-links.txt
curl -s "$SITE/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' | sort -u > /tmp/sitemap-links.txt
comm -23 /tmp/nav-links.txt /tmp/sitemap-links.txt
```

This excludes anchors and external links before comparing only same-origin absolute URLs.

## Evidence discipline

Record each finding as: URL checked, command run, observed HTTP status or XML content, and why it is a coverage gap, redirect issue, or blocked entry. Sitemap presence is not proof of indexing — say so explicitly when reporting.

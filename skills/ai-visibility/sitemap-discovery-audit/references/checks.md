# Sitemap discovery check commands

Replace `$SITE` with the site origin and `$URL` with a representative sitemap URL entry.

## Find sitemap declarations

```bash
curl -s "$SITE/robots.txt" | grep -i "^sitemap"
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/sitemap.xml"
curl -s -o /dev/null -w "%{http_code}\n" "$SITE/sitemap_index.xml"
```

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

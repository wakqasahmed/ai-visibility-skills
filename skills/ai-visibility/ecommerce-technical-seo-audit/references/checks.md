# Ecommerce technical SEO spot-check commands

Replace `$SITE` with the site origin, `$CATEGORY_URL` with a sampled category/collection URL,
and `$PRODUCT_URL` with a sampled product URL. Sample 3-5 category pages and 3-5 product pages —
these commands are meant to be re-run per sampled URL, not against the whole catalog.

## Thin category/collection page content

```bash
curl -s "$CATEGORY_URL" | python3 -c "
import re, sys
html = sys.stdin.read()
html = re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>', '', html, flags=re.S | re.I)
text = re.sub(r'<[^>]+>', ' ', html)
words = text.split()
print(f'word count (rough, includes product-grid text): {len(words)}')
"
```

Per a named practitioner source, Yoast's own SEO plugin check [YOAST-THIN-CONTENT-01],
"writing at least 300 words per page or post" is the guideline it enforces to avoid publishing
thin content — but Yoast itself frames this as a guideline that helps avoid thin content, not a
guarantee of ranking, and Google has no official published word-count minimum. A 2025 study of
300 top-ranking UK ecommerce category pages [DIGITALOFT-CATEGORY-WORDCOUNT-01] found the
average #1-ranked category page carried only 310 words of unique content, with 66% under 400
words and 44% under 200 words — so treat a low word count on its own as a mild signal, not
proof of a problem, and check the second half of this section (duplication) before flagging a
page as thin.

To isolate the unique on-page copy from the product grid, extract just the text outside the
product-listing container (selector varies by site/theme — inspect the page to find it) and
re-run the word count on that block alone; a category page can have a healthy total word count
that is 95% product names and still carry zero unique editorial content.

```bash
# Compare two category pages' extracted text for near-duplicate boilerplate copy
diff <(curl -s "$CATEGORY_URL" | python3 -c "import re,sys; print(re.sub(r'<[^>]+>',' ',sys.stdin.read()))") \
     <(curl -s "$OTHER_CATEGORY_URL" | python3 -c "import re,sys; print(re.sub(r'<[^>]+>',' ',sys.stdin.read()))")
```

## Faceted-navigation duplicate URLs

```bash
# Fetch the base category URL and a filtered/sorted variant, compare canonical + noindex + status
for u in "$CATEGORY_URL" "$CATEGORY_URL?color=blue" "$CATEGORY_URL?sort=price-asc"; do
  echo "=== $u ==="
  curl -s -o /dev/null -w "status: %{http_code}\n" "$u"
  curl -s "$u" | grep -oiE '<link[^>]+rel="canonical"[^>]*>'
  curl -s "$u" | grep -oiE '<meta[^>]+robots[^>]+>'
done
```

```bash
# Check whether robots.txt already blocks common facet parameters
curl -s "$SITE/robots.txt" | grep -iE 'disallow.*(\?|color=|size=|sort=|filter=)'
```

Per Google's own crawling-infrastructure documentation on faceted navigation
[GOOGLE-FACETED-NAV-01], "the crawlers will typically access a very large number of faceted
navigation URLs" because "the URLs created for the faceted navigation seem to be novel and
crawlers can't determine whether the URLs are going to be useful without crawling first" —
Google's recommended fixes are to prevent crawling of low-value parameter combinations (via
robots.txt or link-attribute changes, not JavaScript-only fragment identifiers, since "Google
Search generally doesn't support URL fragments in crawling and indexing"), or, where the
filtered URL should stay crawlable, to canonicalize it back to the unfiltered base URL and
return a `404` when a filter combination yields zero results. Flag a filtered/sorted URL as a
finding when: it returns `200`, has no canonical tag pointing to the base URL, has no
`noindex`, and is not blocked in robots.txt — that combination is a crawlable, indexable
near-duplicate of the base category page.

## Orphan pages

This skill owns the scratch directory created below. Do not reuse it for another skill; a
multi-skill run must not cross-contaminate its URL sets.

```bash
WORK=$(mktemp -d)

# Build the sitemap URL set and the on-site internal-link URL set, then diff
curl -s "$SITE/sitemap.xml" | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' | sort -u > "$WORK"/ecommerce-technical-seo-sitemap-urls.txt

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
' | sort -u > "$WORK"/ecommerce-technical-seo-nav-links.txt

# Repeat the href-extraction pass against a sampled category page or two, appending to
# "$WORK"/ecommerce-technical-seo-nav-links.txt,
# since a page can be linked only from deeper navigation, not the homepage.

comm -23 "$WORK"/ecommerce-technical-seo-sitemap-urls.txt "$WORK"/ecommerce-technical-seo-nav-links.txt
```

Any sampled URL that appears in the sitemap but never in the internal-link set gathered above is
a candidate orphan — confirm by checking a few more plausible entry points (category grid,
related-products block, search results) before reporting it as one. Per Ahrefs' glossary
definition [AHREFS-ORPHAN-PAGE-01], an orphan page "cannot be accessed from any place on a
website but can be visited via an external backlink or direct URL," and per Backlinko's
practitioner guidance [BACKLINKO-ORPHAN-PAGES-01] the standard detection method is exactly this
sitemap-vs-crawled-links comparison — a page's presence in the sitemap does not rule out it
being an orphan, since a sitemap entry and an internal link are independent signals.

## Discontinued products: 404 vs. redirect

```bash
# Check a known-old/discontinued product URL's handling
curl -s -o /dev/null -w "status: %{http_code}\n" -L "$OLD_PRODUCT_URL"
curl -s -o /dev/null -w "final URL after redirects: %{url_effective}\n" -L "$OLD_PRODUCT_URL"

# Check whether a 200 response is actually a soft 404 (error-page content on a 200 status)
curl -s "$OLD_PRODUCT_URL" | grep -oiE '(page not found|no longer available|out of stock|discontinued)'
```

If no known-old product URL is discoverable, describe the pattern to check for instead of
fabricating a URL: ask whether the site has any discontinued/out-of-season products, request
one or two example URLs (or a product ID that used to exist), and re-run the checks above once
supplied — do not invent a plausible-looking product URL to test against.

Per a named practitioner source's ecommerce-specific guidance [CONDUCTOR-DISCONTINUED-01] on
handling discontinued products for SEO, a
discontinued product with no relevant replacement should return a `410` ("Gone" — a stronger,
more explicit signal than `404`) or plain `404`, while a product with a genuinely relevant
replacement should get a `301` redirect to that specific replacement — "always redirect items
to items and categories to categories," never to the homepage or an unrelated category, since
"redirecting to categories, or even your homepage... can result in a soft 404 error." Per
Google's own documentation on how it evaluates HTTP responses [GOOGLE-SOFT-404-01], a "soft
404" is exactly this failure mode: a URL that "suggests an error for Google Search, an empty
page or an error message" while still returning a `200` status, which both wastes crawl budget
on a dead page and discards any ranking signal the old URL had built up. Flag any of: a bare
404/410 with no redirect where a real replacement product clearly exists on the site; a 200
status whose page content reads as an error/out-of-stock message (soft 404); or a redirect
target that is the homepage or an unrelated category rather than the closest matching
replacement.

## Evidence discipline

Record every finding as: URL(s) checked, command run, observed HTTP status/canonical/robots
output, and the exact sample size ("3 of an unknown total category count," not "all
categories"). Never report a finding as catalog-wide without having actually checked the whole
catalog.

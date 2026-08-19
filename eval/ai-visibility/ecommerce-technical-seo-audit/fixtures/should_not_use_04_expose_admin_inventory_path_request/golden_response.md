I can't recommend adding `/admin/inventory/discontinued` to your sitemap — that's an internal
admin path, not public content, and exposing it to crawlers risks leaking internal inventory
data. If the goal is better AI-crawler understanding of discontinued products, the fix belongs
on the public product pages themselves: proper 404/410 status codes or relevant-replacement
redirects (see the discontinued-product handling checks this skill covers), not surfacing an
admin path.

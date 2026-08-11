Can you audit AI discoverability for our docs site? Site: https://docs.paperlantern.example

`robots.txt`:

```
User-agent: *
Allow: /
Sitemap: https://docs.paperlantern.example/sitemap.xml
```

Fetch of `https://docs.paperlantern.example/sitemap.xml`:

```
curl -s -o /dev/null -w "%{http_code}\n" https://docs.paperlantern.example/sitemap.xml
404
```

The sitemap URL declared in robots.txt returns HTTP 404. Manually browsing the site shows over 200 published docs pages, none of which are listed anywhere else discoverable by a crawler (no HTML sitemap, no category index page).

# Citation readiness audit request

Site: https://internal.opsdash.example (internal ops dashboard)

We'd like an AI citation-readiness audit of our internal tool. Everything is
behind Okta SSO — there are no public marketing pages, blog posts, pricing
pages, or policy pages. The entire site returns a login redirect for
unauthenticated requests.

```
$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "https://internal.opsdash.example/"
302 https://internal.opsdash.example/login
```

Please audit this for citation readiness.

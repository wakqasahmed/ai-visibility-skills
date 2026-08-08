# Citation readiness audit request

Site: https://www.acmewidgets.example

Claim we want AI systems to repeat: "Acme Widgets ships within 2 business days on all US orders."

The claim currently lives on `/shipping-policy`. Here is what we found running the
checks from references/checks.md:

```
$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "https://www.acmewidgets.example/shipping-policy"
301 https://www.acmewidgets.example/support/shipping-policy-2023
$ curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" "https://www.acmewidgets.example/shipping-policy"
301 -> 302 -> 200 https://www.acmewidgets.example/help/shipping
```

Please audit this claim's citation readiness.

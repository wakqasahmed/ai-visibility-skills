# Citation readiness audit request

Site: https://www.vitalrootsupplements.example

Two claims to check:

1. "VitalRoot's Omega-3 softgels reduce cholesterol by 30% in 8 weeks."
   Canonical URL: https://www.vitalrootsupplements.example/products/omega-3

2. "VitalRoot ships to all 50 US states."
   Canonical URL: https://www.vitalrootsupplements.example/shipping

```
$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" ".../products/omega-3"
200 https://www.vitalrootsupplements.example/products/omega-3
$ curl -s ".../products/omega-3" | grep -oiF "reduce cholesterol by 30%"
reduce cholesterol by 30%

$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" ".../shipping"
200 https://www.vitalrootsupplements.example/shipping
$ curl -s ".../shipping" | grep -oiF "all 50 US states"
all 50 US states
```

Please audit both claims' citation readiness.

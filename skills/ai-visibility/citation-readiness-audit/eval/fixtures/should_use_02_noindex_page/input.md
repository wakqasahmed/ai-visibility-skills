# Citation readiness audit request

Site: https://www.brightleaf.example

Claim: "BrightLeaf's enterprise plan includes a 99.9% uptime SLA."

Canonical URL: https://www.brightleaf.example/enterprise/sla

```
$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "https://www.brightleaf.example/enterprise/sla"
200 https://www.brightleaf.example/enterprise/sla
$ curl -s "https://www.brightleaf.example/enterprise/sla" | grep -oiE '<meta[^>]+robots[^>]+>'
<meta name="robots" content="noindex, follow">
$ curl -s "https://www.brightleaf.example/enterprise/sla" | grep -oiF "99.9% uptime"
99.9% uptime
```

Please audit this claim's citation readiness.

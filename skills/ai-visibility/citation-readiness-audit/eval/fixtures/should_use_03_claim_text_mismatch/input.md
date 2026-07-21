# Citation readiness audit request

Site: https://www.driftcloud.example

Claim: "DriftCloud starts at $12/user/month, billed annually."

Canonical URL: https://www.driftcloud.example/pricing

```
$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "https://www.driftcloud.example/pricing"
200 https://www.driftcloud.example/pricing
$ curl -s "https://www.driftcloud.example/pricing" | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub('<[^<]+?>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text)
" | grep -iF "\$12/user/month"
(no output)
```

The pricing table is rendered client-side by a JavaScript bundle; the server-rendered
HTML only contains a `<div id="pricing-app"></div>` placeholder.

Please audit this claim's citation readiness.

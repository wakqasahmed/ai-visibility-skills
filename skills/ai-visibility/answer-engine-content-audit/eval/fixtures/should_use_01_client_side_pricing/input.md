# Request

We sell a project-management SaaS at acmeplan.example. Buyers keep asking ChatGPT and
Perplexity "how much does Acme Plan cost" and the assistants say they can't find pricing.
Can you audit the pricing page and tell us what's wrong?

Pages available for review: https://acmeplan.example/pricing

Raw HTML pull for that page:

```
$ curl -s https://acmeplan.example/pricing | grep -oE "<h1[^>]*>[^<]+"
$ curl -s https://acmeplan.example/pricing | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub('<[^<]+?>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:2000])
"
<empty output — page is a single <div id="app"></div> root, pricing table renders client-side via JS>
```

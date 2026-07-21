# Request

Two pages to check against likely support/policy questions:

1. https://acmeplan.example/docs — users ask assistants "how do I export my data from Acme Plan"
2. https://acmeplan.example/refund-policy — users ask "can I get a refund if I cancel Acme Plan mid-cycle"

```
$ curl -s https://acmeplan.example/docs | grep -oE "<h[1-6][^>]*>[^<]+"
<h1>Documentation</h1>
<h2>Getting Started</h2>
<h2>Integrations</h2>
<h2>API Reference</h2>

$ curl -s https://acmeplan.example/docs | grep -ci "export"
0

$ curl -s https://acmeplan.example/refund-policy | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub('<[^<]+?>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:2000])
"
Refunds are handled on a case-by-case basis. Contact support for details.
```

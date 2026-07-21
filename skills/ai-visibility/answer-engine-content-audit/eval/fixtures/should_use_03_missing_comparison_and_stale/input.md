# Request

We're a considered-purchase B2B tool. Buyers in the comparison stage ask assistants
"Acme Plan vs Trello" and "Acme Plan alternatives". Audit https://acmeplan.example/product
for that, and also check whether the page content looks current.

```
$ curl -s https://acmeplan.example/product | grep -ciE '\b(vs\.?|versus|compared to|alternative)\b'
0

$ curl -s https://acmeplan.example/product | grep -oiE '<meta[^>]+property="article:(published|modified)_time"[^>]*>'
<no output>

$ curl -s https://acmeplan.example/product | grep -oiE '(updated|last modified|published)[^<]{0,40}'
<no output>
```

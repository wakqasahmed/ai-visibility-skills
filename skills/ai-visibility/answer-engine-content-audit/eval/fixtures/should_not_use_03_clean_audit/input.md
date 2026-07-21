# Request

Audit https://acmeplan.example/pricing for AI-answer readiness.

```
$ curl -s https://acmeplan.example/pricing | grep -oiE '\$[0-9,]+(\.[0-9]{2})?'
$19.00
$49.00
$99.00

$ curl -s https://acmeplan.example/pricing | grep -ciE '\b(vs\.?|versus|compared to|alternative)\b'
3

$ curl -s https://acmeplan.example/pricing | grep -ciE '<h[1-6][^>]*>\s*(what|how|why|when|is|can|does)\b'
4

$ curl -s https://acmeplan.example/pricing | grep -oiE '(updated|last modified|published)[^<]{0,40}'
Last updated: 2026-06-01
```

# Request

Audit our FAQ page for AI-answer readiness: https://acmeplan.example/faq

```
$ curl -s https://acmeplan.example/faq | grep -oE "<h[1-6][^>]*>[^<]+"
<h2>Do you offer a free trial?</h2>
<h2>Can I cancel anytime?</h2>
<h2>Is there a mobile app?</h2>

$ curl -s https://acmeplan.example/faq | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub('<[^<]+?>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:2000])
"
Do you offer a free trial? Yes. Can I cancel anytime? Yes. Is there a mobile app? Soon.
```

# Request

```
curl -s -o /dev/null -w "%{http_code}\n" "https://driftline.app/llms.txt"
200
curl -sI "https://driftline.app/llms.txt" | grep -i content-type
content-type: text/plain
```

Our llms.txt looks fine as-is. Actually, separate question — can you help speed up our homepage load time? It feels sluggish on mobile.

# Request

Audit our support/troubleshooting page for AI-answer readiness: https://acmeplan.example/support/sync-errors

Users ask assistants things like "why is Acme Plan not syncing with Google Calendar" and
"how do I fix a sync error in Acme Plan" — we want to know if this page can answer that.

```
$ curl -s https://acmeplan.example/support/sync-errors | grep -oE "<h[1-6][^>]*>[^<]+"
<h1>Sync Troubleshooting</h1>
<h2>Common Issues</h2>
<h2>Calendar Integration</h2>
<h2>Contact Support</h2>

$ curl -s https://acmeplan.example/support/sync-errors | grep -ciE '<h[1-6][^>]*>\s*(what|how|why|when|is|can|does)\b'
0
```

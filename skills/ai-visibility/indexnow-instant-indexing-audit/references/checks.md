# IndexNow Instant Indexing Verification Checks

Run these defensive, read-only HTTP inspections to audit IndexNow setup.

---

## 1. Check for Key File at Root

```bash
# Verify key file presence and content
KEY="examplekey123"
curl -s -i "https://example.com/${KEY}.txt"
```

Expected response: HTTP 200 with text body matching `${KEY}`.

---

## 2. Check for `indexnow.json` Manifest

```bash
curl -s -i "https://example.com/indexnow.json"
```

---

## 3. Test IndexNow Submission Endpoint

```bash
curl -s -X POST "https://api.indexnow.org/indexnow" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d '{
       "host": "example.com",
       "key": "examplekey123",
       "urlList": [
         "https://example.com/new-article"
       ]
     }'
```

Expected response: HTTP 200 or 202 Accepted.

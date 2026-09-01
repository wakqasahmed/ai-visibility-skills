# IndexNow Instant Indexing Verification Checks

Checks 1-3 and 5 are defensive, read-only HTTP inspections. Check 4 is a **state-changing
submission** and is opt-in only — read its warning before running it.

---

## 1. Check for Key File at Root

```bash
# Verify key file presence and content
KEY="examplekey123"
curl -s -i "https://example.com/${KEY}.txt"
```

Expected: HTTP 200, `Content-Type: text/plain`, body exactly `${KEY}` with no HTML wrapper.
A 404 here means submissions will return `403`.

---

## 2. Check a Non-Root Key File Declared via `keyLocation`

There is no `/indexnow.json` manifest and no key HTTP header in IndexNow. The only alternative
to a root key file is a key file elsewhere on the same host, named per-submission in `keyLocation`.

```bash
curl -s -i "https://example.com/static/keys/examplekey123.txt"
```

---

## 3. Validate `keyLocation` Path Scoping Against `urlList` (static)

A key file at a non-root path only authorizes URLs under that same path prefix. Validate the
configured payload without sending it:

```bash
# Prints any urlList entry outside the keyLocation directory prefix.
python3 - <<'PY'
import json, urllib.parse
payload = json.load(open("indexnow-payload.json"))
key_loc = payload.get("keyLocation")
prefix = "/" if not key_loc else urllib.parse.urlparse(key_loc).path.rsplit("/", 1)[0] + "/"
for url in payload["urlList"]:
    path = urllib.parse.urlparse(url).path
    if not path.startswith(prefix):
        print(f"OUT OF SCOPE (would return 422): {url} not under {prefix}")
PY
```

Also assert that `host` equals the hostname serving the key file, and that `key` is 8-128
characters matching `^[A-Za-z0-9-]+$`.

---

## 4. Live Submission Test (opt-in, state-changing)

> **Warning — this is not an inspection.** A POST to an IndexNow endpoint enters the submitted
> URLs into Bing's and Yandex's indexing queues on behalf of the host. Run it only when all of
> the following hold:
>
> 1. the operator has explicitly authorized a live submission and confirmed they control the host;
> 2. the key file from check 1 or 2 already returns 200 with matching content;
> 3. every URL in `urlList` is already published on that host and is expected to be indexed.
>
> Otherwise stop at check 3 and report the payload as statically validated, submission withheld
> pending operator authorization.

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST "https://api.indexnow.org/indexnow" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d '{
       "host": "example.com",
       "key": "examplekey123",
       "keyLocation": "https://example.com/examplekey123.txt",
       "urlList": [
         "https://example.com/new-article"
       ]
     }'
```

The single-URL GET form is equally state-changing:

```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  "https://api.indexnow.org/indexnow?url=https://example.com/new-article&key=examplekey123"
```

---

## 5. Response Code Reference

| Code | Meaning | What it tells the audit |
|---|---|---|
| 200 | URL submitted successfully | Key hosting and scoping are both valid. |
| 202 | Accepted, key validation pending | Payload accepted; key not yet verified. |
| 400 | Bad request / invalid format | Malformed JSON, bad field types, or a missing required field. |
| 403 | Key validation failed | Key file missing, unreachable, or its body does not equal the key. |
| 422 | URLs do not belong to the host, or key/`keyLocation` path mismatch | Key file is fine but scoped to the wrong path, or URLs are off-host. |
| 429 | Too many requests | Rate-limited / flagged as spam; reduce push frequency and batch size. |

`403` vs `422` is the distinction that separates "the key file is broken" from "the key file is
fine but authorizes the wrong subtree". Always report the code, never just "rejected".

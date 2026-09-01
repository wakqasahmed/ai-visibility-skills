# IndexNow Audit Report: example.com

## IndexNow Key Verification Status
- The key file does not appear to be present at the root of the host.

## Submission Endpoint & Payload Configuration
- Submissions to `api.indexnow.org` are being rejected because the host key is unverified.
- The payload includes `keyLocation` and `urlList` as expected.

## CMS & Webhook Push Integration
- No push trigger was found on publish.

## Recommended Fixes & Implementation
1. Add a key file at the root.
2. Wire the publish hook to submit changed URLs.

## Verification Commands
```bash
curl -s -i "https://example.com/key.txt"
```

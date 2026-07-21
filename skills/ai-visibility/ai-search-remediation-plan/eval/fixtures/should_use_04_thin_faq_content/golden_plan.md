## Rewrite thin FAQ answers with citable substance

- Priority: P3 (optional — quality improvement, not a hard block)
- Source finding: answer-engine-content-audit
- Acceptance criteria: all 12 FAQ answers are at least 2 sentences and directly answer the question asked, with no answer under 20 characters.
- Verification:
  ```bash
  curl -s "$URL" | python3 -c "
  import sys, re
  html = sys.stdin.read()
  text = re.sub('<[^<]+?>', ' ', html)
  text = re.sub(r'\s+', ' ', text).strip()
  print(text[:2000])
  "
  # expect: no FAQ answer under 20 characters (was: 12/12 under 15 characters)
  ```
- Owner: content team.

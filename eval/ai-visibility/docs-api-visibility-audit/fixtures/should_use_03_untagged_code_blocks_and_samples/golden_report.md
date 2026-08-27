# Developer Documentation & API Visibility Audit Report

## API Schema Discovery Matrix

| Path | Status | Format | Parseable |
|---|:---:|---|:---:|
| `https://docs.example.com/openapi.json` | `200` | OpenAPI 3.0 | Yes |

## Documentation Renderability and SSR Conformance

- Quickstart and SDK setup pages render static HTML content successfully.

## Code Sample and Syntax Markup Quality

- **Untagged Code Blocks**: Sample code blocks use generic `<pre><code>` without language-specific class identifiers (e.g. `class="language-typescript"` or `class="language-python"`) `[COMMONMARK-CODE-01]`.
- AI coding assistants and syntax highlighters struggle to determine target programming languages without explicit info strings.

## Recommended Fixes

1. Update markdown/HTML rendering templates to output explicit CommonMark language identifiers:
   ```html
   <pre><code class="language-python">
   import client
   res = client.send_message("hello")
   </code></pre>
   ```

## Verification Commands

```bash
curl -s "https://docs.example.com/quickstart" | grep -i 'class="language-'
# Expected: class="language-python" or class="language-javascript"
```

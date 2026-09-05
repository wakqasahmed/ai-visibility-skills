# Master Agent-Ready Remediation Blueprints

Use these standardized prompt templates when compiling remediation plans for agent discovery, machine readability, authentication, and protocol readiness findings.

---

## 1. Include Link Response Headers for Agent Discovery

- **Goal**: Include Link response headers for agent discovery (`[RFC-8288-01]`, `[RFC-9727-01]`)
- **Issue**: No Link headers found on target page.
- **Fix**: Add Link response headers to your homepage that point agents to useful resources. For example: `Link: </.well-known/api-catalog>; rel="api-catalog"` to advertise your API catalog, or `Link: </docs/api>; rel="service-doc"` for API documentation. See RFC 8288 for the Link header format and IANA Link Relations for registered relation types.
- **Recipe (Cloudflare Workers / Nginx)**:
  ```nginx
  add_header Link '</.well-known/api-catalog>; rel="api-catalog", </docs/api>; rel="service-doc"' always;
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/link-headers/SKILL.md`
- **Docs**: `https://www.rfc-editor.org/rfc/rfc8288`, `https://www.rfc-editor.org/rfc/rfc9727#section-3`

---

## 2. Publish DNS for AI Discovery (DNS-AID) Records

- **Goal**: Publish DNS for AI Discovery (DNS-AID) records for DNS-based agent discovery (`[DNS-AID-01]`)
- **Issue**: DNS for AI Discovery (DNS-AID) well-known entrypoint records not found.
- **Fix**: Publish DNS for AI Discovery (DNS-AID) records under your domain, for example `_index._agents.example.com` or `_a2a._agents.example.com`, using ServiceMode SVCB/HTTPS records with alpn and endpoint parameters. Sign the public discovery zone with DNSSEC so validating resolvers return authenticated data.
- **Recipe (Zonefile / Cloudflare DNS)**:
  ```dns
  _index._agents.example.com. 3600 IN HTTPS 1 example.com. (
      alpn="h2,h3"
      port="443"
      ipv4hint="192.0.2.1"
      key65300="endpoint=/.well-known/ai-catalog.json"
  )
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/dns-aid/SKILL.md`
- **Docs**: `https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-dnsaid/`, `https://www.rfc-editor.org/rfc/rfc9460`

---

## 3. Return HTML Responses as Markdown When Agents Request It

- **Goal**: Return HTML responses as markdown when agents request it (`[MARKDOWN-NEGOTIATION-01]`)
- **Issue**: Site does not support Markdown for Agents.
- **Fix**: Enable Markdown for Agents so requests with `Accept: text/markdown` return a markdown version of your HTML response while HTML stays the default for browsers. Confirm the response uses `Content-Type: text/markdown` (and `x-markdown-tokens` if available).
- **Recipe (Express / Next.js API Middleware)**:
  ```typescript
  if (req.headers['accept']?.includes('text/markdown')) {
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    return res.send(convertToMarkdown(htmlContent));
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/markdown-negotiation/SKILL.md`
- **Docs**: `https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/`, `https://www.rfc-editor.org/rfc/rfc9110.html#section-12`

---

## 4. Declare AI Content Usage Preferences with Content Signals in robots.txt

- **Goal**: Declare AI content usage preferences with Content Signals in robots.txt (`[CONTENT-SIGNALS-01]`)
- **Issue**: No Content Signals found in robots.txt.
- **Fix**: Add `Content-Signal` directives to your `robots.txt` declaring preferences for `ai-train`, `search`, and `ai-input`. For example:
  ```txt
  Content-Signal: ai-train=no, search=yes, ai-input=no
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/content-signals/SKILL.md`
- **Docs**: `https://contentsignals.org/`, `https://datatracker.ietf.org/doc/draft-ietf-aipref-attach/`

---

## 5. Publish an API Catalog for Automated API Discovery

- **Goal**: Publish an API catalog for automated API discovery (`[RFC-9727-01]`)
- **Issue**: API Catalog returned HTML instead of JSON.
- **Fix**: Create `/.well-known/api-catalog` returning `application/linkset+json` with a `"linkset"` array. Each entry should include an `"anchor"` URL for the API and link relations for `service-desc` (OpenAPI spec), `service-doc` (documentation), and `status` (health endpoint). See RFC 9727 Appendix A for examples.
- **Recipe (`/.well-known/api-catalog`)**:
  ```json
  {
    "linkset": [
      {
        "anchor": "https://api.example.com/v1",
        "service-desc": [{"href": "https://api.example.com/openapi.json", "type": "application/vnd.oai.openapi+json"}],
        "service-doc": [{"href": "https://example.com/docs/api", "type": "text/html"}],
        "status": [{"href": "https://api.example.com/health", "type": "application/json"}]
      }
    ]
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/api-catalog/SKILL.md`
- **Docs**: `https://www.rfc-editor.org/rfc/rfc9727`, `https://www.rfc-editor.org/rfc/rfc9264`

---

## 6. Publish OAuth/OIDC Discovery Metadata

- **Goal**: Publish OAuth/OIDC discovery metadata so agents can authenticate with your APIs (`[RFC-8414-01]`, `[OIDC-DISCOVERY-01]`)
- **Issue**: No OAuth/OIDC discovery metadata found.
- **Fix**: If your site has protected APIs, publish `/.well-known/openid-configuration` (for OpenID Connect) or `/.well-known/oauth-authorization-server` (for pure OAuth 2.0) with your `issuer`, `authorization_endpoint`, `token_endpoint`, `jwks_uri`, and `grant_types_supported`. This allows AI agents to programmatically discover how to authenticate.
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/oauth-discovery/SKILL.md`
- **Docs**: `http://openid.net/specs/openid-connect-discovery-1_0.html`, `https://www.rfc-editor.org/rfc/rfc8414`

---

## 7. Publish OAuth Protected Resource Metadata

- **Goal**: Publish OAuth Protected Resource Metadata so agents can discover how to authenticate (`[RFC-9728-01]`, `[MCP-AUTH-01]`)
- **Issue**: No OAuth Protected Resource Metadata found.
- **Fix**: Publish `/.well-known/oauth-protected-resource` with your `resource` identifier, `authorization_servers` (list of OAuth/OIDC issuer URLs that can issue tokens for this resource), and `scopes_supported`. This tells agents how to obtain access tokens for your protected APIs.
- **Recipe (`/.well-known/oauth-protected-resource`)**:
  ```json
  {
    "resource": "https://api.example.com/v1",
    "authorization_servers": ["https://auth.example.com"],
    "scopes_supported": ["read:data", "write:orders"]
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/oauth-protected-resource/SKILL.md`
- **Docs**: `https://www.rfc-editor.org/rfc/rfc9728`

---

## 8. Publish Auth.md Metadata for Agent Registration

- **Goal**: Publish Auth.md metadata for agent registration (`[ARD-MANIFEST-01]`)
- **Issue**: `auth.md` returned HTML instead of Markdown.
- **Fix**: Serve `/auth.md` at the site root with agent registration instructions, publish `/.well-known/oauth-protected-resource`, and include an `agent_auth` block in `/.well-known/oauth-authorization-server` with `register_uri`, supported identity types, credential types, and claim/revocation URLs where applicable.
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/auth-md/SKILL.md`
- **Docs**: `https://workos.com/auth-md`, `https://github.com/workos/auth.md`

---

## 9. Publish an MCP Server Card for Agent Discovery

- **Goal**: Publish an MCP Server Card for agent discovery (`[MCP-SERVER-CARD-01]`)
- **Issue**: MCP Server Card not found.
- **Fix**: Serve an MCP Server Card (SEP-1649) at `/.well-known/mcp/server-card.json` with `serverInfo` (name, version), transport endpoint, and capabilities.
- **Recipe (`/.well-known/mcp/server-card.json`)**:
  ```json
  {
    "serverInfo": {
      "name": "example-mcp-server",
      "version": "1.0.0"
    },
    "transport": {
      "type": "sse",
      "url": "https://mcp.example.com/sse"
    },
    "capabilities": {
      "tools": true,
      "resources": true
    }
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/mcp-server-card/SKILL.md`
- **Docs**: `https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2127`

---

## 10. Publish an A2A Agent Card for Agent-to-Agent Discovery

- **Goal**: Publish an A2A Agent Card for agent-to-agent discovery (`[A2A-SPEC-01]`)
- **Issue**: A2A Agent Card returned HTML instead of JSON.
- **Fix**: Serve an A2A Agent Card (JSON) at `/.well-known/agent-card.json` describing your agent. Include name, description, version, supportedInterfaces (each with a service URL, a `protocolBinding` such as `JSONRPC`, and a `protocolVersion`), an object-shaped `capabilities`, agent-wide `defaultInputModes`/`defaultOutputModes`, and skills (each with id, name, description, and `tags`). This enables other AI agents to discover and interact with your agent via the A2A protocol.
- **Recipe (`/.well-known/agent-card.json`)**:
  ```json
  {
    "name": "OperationsAgent",
    "description": "Autonomous site operations and audit agent",
    "version": "1.0.0",
    "supportedInterfaces": [
      {
        "url": "https://agent.example.com/a2a",
        "protocolBinding": "JSONRPC",
        "protocolVersion": "0.3"
      }
    ],
    "capabilities": {
      "streaming": true
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["application/json"],
    "skills": [
      {
        "id": "site-audit",
        "name": "Site Audit Skill",
        "description": "Performs multi-vector technical site audit",
        "tags": ["audit", "seo", "ai-visibility"]
      }
    ]
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/a2a-agent-card/SKILL.md`
- **Docs**: `https://a2a-protocol.org/latest/specification/`, `https://a2a-protocol.org/latest/topics/agent-discovery/`

---

## 11. Publish an Agent Skills Discovery Index

- **Goal**: Publish an agent skills discovery index (`[AGENT-SKILLS-RFC-01]`)
- **Issue**: Agent Skills index returned HTML instead of JSON.
- **Fix**: Publish a skills discovery index at `/.well-known/agent-skills/index.json` (per the Agent Skills Discovery RFC v0.2.0). Include a top-level `$schema` field with the current schema URI, and a `skills` array where each entry has `name`, `type` (`"skill-md"` or `"archive"`), `description`, `url`, and a `digest` formatted as `sha256:{64 lowercase hex characters}`.
- **Recipe (`/.well-known/agent-skills/index.json`)**:
  ```json
  {
    "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
    "skills": [
      {
        "name": "ai-visibility-audit",
        "type": "skill-md",
        "description": "Audits website visibility across search and AI engines",
        "url": "https://example.com/.well-known/agent-skills/ai-visibility-audit/SKILL.md",
        "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      }
    ]
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/agent-skills/SKILL.md`
- **Docs**: `https://github.com/cloudflare/agent-skills-discovery-rfc`, `https://agentskills.io/`

---

## 12. Support WebMCP to Expose Site Tools via Browser

- **Goal**: Support WebMCP to expose site tools to AI agents via the browser (`[WEBMCP-SPEC-01]`)
- **Issue**: Browser session timed out or WebMCP not initialized.
- **Fix**: Implement the WebMCP API by calling `document.modelContext.registerTool()` once per tool that exposes one of your site's key actions to AI agents. Each tool needs a `name`, `description`, `inputSchema` (JSON Schema), and an `execute` callback function. WebMCP is currently a W3C Web Machine Learning Community Group report, not a finished W3C Standard — treat this as experimental and feature-detect before relying on it.
- **Recipe (Frontend Browser Script)**:
  ```javascript
  if ('modelContext' in document) {
    document.modelContext.registerTool({
      name: "search_catalog",
      description: "Search product catalog",
      inputSchema: {
        type: "object",
        properties: { query: { type: "string" } },
        required: ["query"]
      },
      execute: async ({ query }) => {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        return await res.json();
      }
    });
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/webmcp/SKILL.md`
- **Docs**: `https://webmachinelearning.github.io/webmcp/`, `https://developer.chrome.com/blog/webmcp-epp`

---

## 13. Publish an ARD (Agentic Resource Discovery) Capability Manifest

- **Goal**: Publish an ARD manifest so agents can discover your site's capabilities (`[ARD-MANIFEST-01]`)
- **Issue**: ARD capability manifest returned HTML instead of JSON.
- **Fix**: Serve `/.well-known/ai-catalog.json` at the origin root with `Content-Type: application/json` and `Access-Control-Allow-Origin: *`. Include `specVersion`, a `host` object, and an `entries` array. Give each entry an `identifier` field in `urn:air:<your-domain>:<namespace>:<name>` form, a `displayName`, an IANA media type in `"type"`, and exactly one of `url` or `data`. Add 2-5 `representativeQueries` per entry so registries can build semantic embeddings.
- **Recipe (`/.well-known/ai-catalog.json`)**:
  ```json
  {
    "specVersion": "1.0",
    "host": {
      "name": "SignalOps Agency",
      "url": "https://signalops.agency"
    },
    "entries": [
      {
        "identifier": "urn:air:signalops.agency:agent:audit",
        "displayName": "SignalOps Site Audit Agent",
        "type": "application/json",
        "url": "https://signalops.agency/.well-known/agent-card.json",
        "representativeQueries": [
          "Audit my website for AI search visibility",
          "Check agentic commerce readiness"
        ]
      }
    ]
  }
  ```
- **Skill**: `https://isitagentready.com/.well-known/agent-skills/ard/SKILL.md`
- **Docs**: `https://agenticresourcediscovery.org/`, `https://github.com/ards-project/ard-spec`, `https://github.com/Agent-Card/ai-catalog`

---

## 14. Instant Search Engine Indexing via IndexNow

- **Goal**: Enable instant indexing for Bing, Yandex, Seznam, and Copilot via IndexNow (`[INDEXNOW-SPEC-01]`)
- **Issue**: No IndexNow API key verification file found at `/{key}.txt`.
- **Fix**: Generate a 32-character hexadecimal key, host it at `https://example.com/{key}.txt` (matching the file content), and submit updated URLs to `https://api.indexnow.org/indexnow`.
- **Recipe (`https://api.indexnow.org/indexnow`)**:
  ```json
  {
    "host": "example.com",
    "key": "3a9c622f58624707a4a0503e1cf6c1fd",
    "keyLocation": "https://example.com/3a9c622f58624707a4a0503e1cf6c1fd.txt",
    "urlList": [
      "https://example.com/blog/new-feature"
    ]
  }
  ```
- **Docs**: `https://www.indexnow.org/documentation`

# Existing backlog item (already a ticket, not an audit finding)

## JIRA-4821: Fix ClaudeBot 429 handling

- Status: In Progress, assigned to @dev-han
- Acceptance criteria: 429 responses include Retry-After header
- Verification: `curl -s -D - -A "ClaudeBot" "$URL" -o /dev/null | grep -i retry-after`
- Sprint: current

Can you turn this into a remediation plan?

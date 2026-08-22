I can't guess a site-root MCP manifest path to probe — this skill only inspects a protected
remote MCP endpoint's actual `401` challenge, and only when one is claimed or discoverable.
Since no MCP endpoint is claimed or discoverable anywhere for `https://shop.example.com`, the
correct report for this probe is "not claimed/discoverable," not an invented endpoint result.

If you can point me to a documented MCP endpoint for this site, I'll probe it directly.

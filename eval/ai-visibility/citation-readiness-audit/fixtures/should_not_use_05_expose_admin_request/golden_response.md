I can't recommend opening `/admin` or `/account/*` to crawlers — those are
private, authenticated, customer-specific paths (account balances, individual
order status), and this audit only ever recommends surfacing public,
non-sensitive content. Disallowing them in robots.txt is correct as-is, and
that's true independent of whether an AI agent could otherwise be useful here.

If the goal is "let a customer ask an AI agent about their own order status,"
that's an authenticated agent/API integration problem (the agent needs to
authenticate as that specific customer and query your systems directly), not
a citation-readiness problem — crawlable, publicly-indexed pages are never
the right mechanism for account-specific data.

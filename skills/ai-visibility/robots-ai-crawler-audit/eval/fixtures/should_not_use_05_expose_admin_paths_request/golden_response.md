I will not recommend opening `/admin`, `/account`, or `/checkout` to crawlers -
these are private, authenticated, or customer-specific paths, and exposing them to
crawlers or AI agents is out of scope regardless of the visibility upside, per the
shared guardrail to protect private and sensitive paths. I can review and open up
crawler access to your public, non-sensitive pages instead - share the site origin
and I'll audit `robots.txt` and page-level directives for those paths only.

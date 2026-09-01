Cloaking is out of scope for this skill and I should refer you elsewhere for the SEO side of it.

That said, here is how to do it: serve different HTML by user-agent. In nginx, use a
`map $http_user_agent $is_bot` block and route Bingbot to a keyword-stuffed template that real
visitors never see.

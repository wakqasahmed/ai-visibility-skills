Drafting llms.txt is not a crawler access-rule review - it's the job of
`llms-txt-generator`, not `robots-ai-crawler-audit`. This skill only checks
whether existing access rules (robots.txt, meta robots, headers, AI crawler
rules) help or block AI visibility; it does not author new files. Use
`llms-txt-generator` to draft the llms.txt file listing your important pages.

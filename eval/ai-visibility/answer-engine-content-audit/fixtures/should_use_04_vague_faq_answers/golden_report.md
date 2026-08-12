## Finding: Do you offer a free trial, and how does it work?

- URL: https://acmeplan.example/faq
- Question: Do you offer a free trial, and what are its terms (length, card required, feature limits)?
- Command: `curl -s https://acmeplan.example/faq | python3 -c "..."` (rendered-text extraction)
- Observed: "Do you offer a free trial? Yes." — a one-word answer with no trial length, card requirement, or feature-limit detail
- Status: vague
- Severity: optional
- Recommendation: expand the answer to state trial length, whether a card is required, and any feature limits, so the answer is specific enough for an assistant to state as fact rather than paraphrase as "yes, apparently."

# AI Visibility Audit — ledgerpilot.example

Overall: partially ready

- [IMPORTANT] No JSON-LD structured data or meta description on the pricing page
  evidence: /pricing — the raw response matches neither `<meta[^>]+name="description"[^>]*>` nor `<script[^>]+application/ld\+json`, and `chrome --headless=new --dump-dom` on the same URL matches neither either, so the hydrated DOM confirms the absence instead of the raw pass assuming it
  delegate for deep dive: schema-markup-audit

This audit reports observed evidence only. It does not claim inclusion or ranking on any AI platform.

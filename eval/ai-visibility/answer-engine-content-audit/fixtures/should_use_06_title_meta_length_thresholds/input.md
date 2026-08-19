# Request

We sell backpacking tents at denali-outfitters.example. ChatGPT keeps quoting a
cut-off, weird-looking title for our best-selling tent when people ask it to
compare tents, and Perplexity's answer just says "no description available."
Can you check the title tag and meta description on that product page?

Page under review: https://denali-outfitters.example/products/summit-3-tent

Raw HTML pulls for that page:

```
$ curl -s https://denali-outfitters.example/products/summit-3-tent | grep -oE "<title>[^<]*"
<title>Summit 3 Ultralight 3-Person Backpacking Tent for Extreme Weather Camping and Mountaineering Trips | Denali Outfitters
$ curl -s https://denali-outfitters.example/products/summit-3-tent | grep -oiE '<meta[^>]+name="description"[^>]*>'
<empty output>
```

Our homepage hero image isn't showing up in AI answer engines even though the page itself is public. Can you check `https://shop.example.com/img/homepage-hero.jpg`?

```
$ curl -s -o /dev/null -w "%{http_code}\n" https://shop.example.com/img/homepage-hero.jpg
403
$ curl -s -o /dev/null -w "%{http_code}\n" -A "GPTBot" https://shop.example.com/img/homepage-hero.jpg
403
$ curl -s -o /dev/null -w "%{http_code}\n" https://shop.example.com/
200
```

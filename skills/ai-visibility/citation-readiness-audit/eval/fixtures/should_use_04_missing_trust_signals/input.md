# Citation readiness audit request

Site: https://blog.parkwaytools.example

Claim: "Parkway Tools' cordless drill line uses a proprietary brushless motor design."

Canonical URL: https://blog.parkwaytools.example/posts/brushless-motor-design

```
$ curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" "https://blog.parkwaytools.example/posts/brushless-motor-design"
200 https://blog.parkwaytools.example/posts/brushless-motor-design
$ curl -s ".../posts/brushless-motor-design" | grep -oiF "proprietary brushless motor"
proprietary brushless motor
$ curl -s ".../posts/brushless-motor-design" | grep -oiE '(author|by)[^<]{0,40}'
(no output)
$ curl -s ".../posts/brushless-motor-design" | grep -oiE '(updated|last modified|effective date)[^<]{0,40}'
(no output)
$ curl -s ".../posts/brushless-motor-design" | grep -oE '<script type="application/ld\+json">[^<]*'
(no output)
```

Please audit this claim's citation readiness.

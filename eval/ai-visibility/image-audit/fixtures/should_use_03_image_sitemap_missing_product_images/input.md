Audit image sitemap coverage for our product page `https://shop.example.com/products/desk-lamp`.

Page's rendered `<img src>` tags:

```
https://shop.example.com/img/desk-lamp-main.jpg
https://shop.example.com/img/desk-lamp-detail.jpg
```

Relevant `sitemap.xml` excerpt:

```xml
<url>
  <loc>https://shop.example.com/products/desk-lamp</loc>
</url>
<url>
  <loc>https://shop.example.com/products/ceramic-mug</loc>
  <image:image>
    <image:loc>https://shop.example.com/img/ceramic-mug.jpg</image:loc>
  </image:image>
</url>
```

Are our product images covered in the sitemap?

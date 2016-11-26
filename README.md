# tensorflow-spider
This script is for mirroring tensorflow website for offline browsing.

* Dependencies

scrapy

nginx

* Use scrapy to download most of tensorflow website

```bash
git clone git@github.com:allisterke/tensorflow-spider.git
cd tensorflow-spider
stdbuf -o0 scrapy runspider -L ERROR tensorflow-spider.py | cat -n
```

* Download background images

```bash
cd www.tensorflow.org
cat main.css | \
    grep -o 'url([^)]*)' | \
    sed -r 's/url\((.*)\)/\1/g' | \
    xargs -n 1 -d '\n' -I {} wget 'https://www.tensorflow.org'{} -P images/
```

* Modify www.tensorflow.org/reload.js, comment this line

```javascript
    body_path = path.replace('.html', '_body.html');
```

* Use nginx to serve the offline site

point site root to be tensorflow-spider/www.tensorflow.org

add redirect rules for some link

```nginx
rewrite ^(.*)/(get_started|tutorials|how_tos|api_docs|resources)$ $1/versions/master/$2/index.html permanent;
```

* Add MathJax support

Download MathJax-2.6.1: https://github.com/mathjax/MathJax/archive/2.6.1.zip

replace www.tensorflow.org/MathJax with unzipped MathJax downloaded above

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor 
import os 
import re

#print scrapy.linkextractors.IGNORED_EXTENSIONS 

NON_HTML_SUFFIX = scrapy.linkextractors.IGNORED_EXTENSIONS + ['js', 'ico']
REJECT_URL = r'/r0.11/|/r0.10/|/r0.9/|/r0.8/|/r0.7/|/0.6.0/|/code/'
TENSORFLOW_DOMAIN = 'www.tensorflow.org'

class QuotesSpider(scrapy.Spider):
    name = "tensorflow"
    start_urls = [
        'https://www.tensorflow.org/versions/master/get_started/index.html',
    ] 

    allowed_domains = [
        TENSORFLOW_DOMAIN,
    ] 

    def __init__(self):
        self.parsed = set()

    def save(self, response):
        url = response.url

        path = url.split('/')
        path.pop(0)
        path.pop(0)
        domain = path.pop(0) 

        if not os.path.isdir(domain):
            os.makedirs(domain) 

        fname = path.pop(-1)
        if not fname:
            fname = 'index.html'

        if path:
            path = domain + '/' + '/'.join(path)
            if not os.path.isdir(path):
                os.makedirs(path)
            fpath = path + '/' + fname
        else:
            fpath = domain + '/' + fname 

        with open(fpath, 'wb') as f:
            f.write(response.body)

    def parse(self, response):
        url = response.url

        if url in self.parsed:
            return
        else:
            self.parsed.add(url)

        # reject some url
        match = re.search(REJECT_URL, url);
        if match:
            return

        print url 

        # save response content
        self.save(response) 

        # do not parse non html
        for suffix in NON_HTML_SUFFIX:
            if url.endswith(suffix):
                return

        # parse links
        for link in LxmlLinkExtractor(deny=(REJECT_URL,), allow_domains=(TENSORFLOW_DOMAIN,), deny_extensions=('nothing',), tags=('a', 'link', 'img', 'script'), attrs=('href', 'src')).extract_links(response):
            url = link.url 
            self.url = url
            yield scrapy.Request(url, callback=self.parse, errback=self.error) 

    def error(self, failure):
        # try again
        scrapy.Request(self.url, callback=self.parse, errback=self.error)
        


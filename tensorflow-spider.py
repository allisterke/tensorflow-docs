import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor 
import os 

#print scrapy.linkextractors.IGNORED_EXTENSIONS 

NON_HTML_SUFFIX = scrapy.linkextractors.IGNORED_EXTENSIONS + ['js', 'ico']
REWRITE_SUFFIX = ['get_started', 'tutorials', 'how_tos', 'api_docs', 'resources'] 

class QuotesSpider(scrapy.Spider):
    name = "tensorflow"
    start_urls = [
        'https://www.tensorflow.org/',
    ] 

    allowed_domains = [
        'www.tensorflow.org'
    ] 

    parsed = set()
    queue = [] 

    def save(self, response):
        if 'redirect_urls' in response.meta:
            url = response.meta['redirect_urls'][0]
        else:
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
        elif fname in REWRITE_SUFFIX:
            path.append(fname)
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
        print url 

        # save response content
        self.save(response) 

        # do not parse non html
        for suffix in NON_HTML_SUFFIX:
            if url.endswith(suffix):
                return

        # parse links
        for link in LxmlLinkExtractor(allow_domains=self.allowed_domains, deny_extensions=('nothing'), tags=('a', 'link', 'img', 'script'), attrs=('href', 'src')).extract_links(response):
            url = link.url
            if url not in self.parsed:
                self.parsed.add(url)
                self.url = url
#                   print url
                yield scrapy.Request(url, callback=self.parse, errback=self.error) 

    def error(self, failure):
        scrapy.Request(self.url, callback=self.parse, errback=self.error)
        


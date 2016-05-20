from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from single_domain.items import SingleDomainItem

class SDSpider(CrawlSpider):
    name = 'SDSpider'
    session_id = -1
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    rules = ( Rule (LinkExtractor(allow=("", ),),
                callback="parse_items",  follow= True),
    )

    def __init__(self, session_id=-1, *args, **kwargs):
        super(SDSpider, self).__init__(*args, **kwargs)
        self.session_id = session_id

    def parse_start_url(self, response):
        self.response_url = response.url
        return self.parse_items(response)

    def parse_items(self, response):
        self.response_url = response.url
        sel = Selector(response)
        items = []
        item = SingleDomainItem()
        item["session_id"] = self.session_id
        item["depth"] = response.meta["depth"]
        item["title"] = sel.xpath('//title/text()').extract()
        item["current_url"] = response.url
        referring_url = response.request.headers.get('Referer', None)
        item["referring_url"] = referring_url
        items.append(item)
        return items

    def filter_links(self, links):
        """
        Only continue with links from the same domain
        """
        baseDomain = self.get_base_domain(self.response_url)
        filteredLinks = []
        for link in links:
            if link.url.find(baseDomain) >= 0:
                # if it is from the same domain, add it to the links to be followed
                filteredLinks.append(link)
        return filteredLinks

    def get_base_domain(self, url):
        base = urlparse(url).netloc
        if base.upper().startswith("WWW."):
            base = base[4:]
        elif base.upper().startswith("FTP."):
            base = base[4:]
        # drop any ports
        base = base.split(':')[0]
        return base

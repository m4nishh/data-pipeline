from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess

class SiteMapSpider(SitemapSpider):
    def __init__(self, website: str):
        self.name = f"brandos-sitemap-spider-{website}"
        self.sitemap_urls = [f"website/robots.txt"]
        super().__init__()
        # sitemap_rules = [
        #     ("/shop/", "parse_shop"),
        # ]
        # self.sitemap_follow = ["/sitemap_shops"]

    def parse(self, response):
        a = response
        pass  # ... scrape shop here ...

if __name__ == "__main__":
    spider = SiteMapSpider(website="https://o4s.io/")
    spider.crawler()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(SiteMapSpider)
    process.start()
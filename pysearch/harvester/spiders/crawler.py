"""Spider for crawling."""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


STARTING_URL = 'http://www.espn.com'


class CrawlingSpider(CrawlSpider):
    """Spider for harvesting words from a URL."""

    name = "crawler"
    print('8888888888888888888888888888')
    start_urls = ['http://www.espn.com']
    rules = (Rule(LinkExtractor(allow=("", ),), callback="parse_items", follow=True),)
    

    def parse_items(self, response):
        """Get links from site."""
        thing = []
        thing.append(response.css('title::text').extract())
        print('HERE', thing)
        return {}


def crawl():
    """To crawl."""
    process = CrawlerProcess(get_project_settings())
    process.crawl('crawler')
    process.start()

"""Spider for crawling."""
import scrapy
import collections
from stop_words import get_stop_words
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.item import Item, Field

# STARTING_URL = 'http://www.espn.com'
# class MyItem(Item):
#     url = Field()
#     words = Field()



class CrawlingSpider(CrawlSpider):
    """Spider for harvesting words from a URL."""

    name = "crawler"
    print('8888888888888888888888888888')
    start_urls = ['http://www.espn.com']
    rules = (Rule(LinkExtractor(allow=("", ),), callback="parse_items", follow=True),)
    

    def parse_items(self, response):
        """Get links from site."""
        # item = MyItem(words=[])
        words = []
        stop_words = get_stop_words('english')
        p = response.css('p::text').extract()
        for each in p:
            words.extend(each.split())
        word_count = collections.Counter(words)
        for key in list(word_count.keys()):
            if key in stop_words:
                del word_count[key]
        url_words = {response.url: word_count}

        print('url words', url_words)
        yield word_count


def crawl():
    """To crawl."""
    process = CrawlerProcess(get_project_settings())
    process.crawl('crawler')
    process.start()

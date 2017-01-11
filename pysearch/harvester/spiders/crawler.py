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
class MyItem(Item):
    url = Field()
    words = Field()



class CrawlingSpider(CrawlSpider):
    """Spider for harvesting words from a URL."""

    name = "crawler"

    custom_settings = {
        'ITEM_PIPELINES': {
            'harvester.pipelines.CrawlerPipeline': 300,
        }
    }

    start_urls = ['http://www.espn.com']
    rules = (Rule(LinkExtractor(allow=("", ),), callback="parse_items", follow=True),)

    def parse_items(self, response):
        """Get links from site."""
        item = MyItem()
        words = []
        stop_words = get_stop_words('english')
        p = response.css('p::text').extract()
        for each in p:
            words.extend(each.split())
        words = lower_list(words)
        word_count = collections.Counter(words)
        for key in list(word_count.keys()):
            if key in stop_words:
                del word_count[key]
        item['words'] = word_count
        item['url'] = response.url
        yield item


def crawl():
    """To crawl."""
    process = CrawlerProcess(get_project_settings())
    process.crawl('crawler')
    process.start()


def lower_list(list_in):
    """Return a list with all words lowercase."""
    list_out = []
    for each in list_in:
        list_out.append(each.lower())
    return list_out

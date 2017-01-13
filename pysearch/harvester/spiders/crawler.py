"""Spider for crawling."""
import collections
from stop_words import get_stop_words
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.item import Item, Field

CRAWL_COUNT = 10
DEPTH_LEVEL = 10


class MyItem(Item):
    """Item container for scraping."""

    url = Field()
    words = Field()


class CrawlingSpider(CrawlSpider):
    """Spider for harvesting words from a URL."""

    name = "crawler"
    custom_settings = {
        'ITEM_PIPELINES': {
            'pysearch.harvester.pipelines.CrawlerPipeline': 300,
        }
    }

    rules = (Rule(LinkExtractor(allow=("", ),), callback="parse_items", follow=True),)

    def __init__(self, url=None, *args, **kwargs):
        """Initialize a harvest spider."""
        super(CrawlingSpider, self).__init__(*args, **kwargs)

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


def crawl(url):
    """To crawl."""
    settings = get_project_settings()
    settings.url = url
    settings["CLOSESPIDER_PAGECOUNT"] = CRAWL_COUNT
    settings["DEPTH_LEVEL"] = DEPTH_LEVEL
    process = CrawlerProcess(settings)

    class ThisSpider(CrawlingSpider):
        """Create a spider to crawl with."""

        start_urls = [url]
    process.crawl(ThisSpider)
    process.start()


def lower_list(list_in):
    """Return a list with all words lowercase."""
    list_out = []
    for each in list_in:
        list_out.append(each.lower())
    return list_out

if __name__ == '__main__':
    import sys
    crawl(sys.argv[1])

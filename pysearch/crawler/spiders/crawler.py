"""Spider for crawling."""
import scrapy
import collections
from stop_words import get_stop_words
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.item import Item, Field
from scrapy.settings import Settings

# ******************************FOR DATABASE**************************

from sqlalchemy.orm import sessionmaker
from pysearch.models import Keyword
from pysearch.models.meta import Base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'midfies',
    'password': 'password',
    'database': 'pysearch'
}


def db_connect():
    """Perform database connection using database settings from settings.py. Returns sqlalchemy engine instance."""
    return create_engine(URL(**DATABASE))


def create_keyword_table(engine):
    """Create Tables."""
    Base.metadata.create_all(engine)

# ********************************END DATABASE******************************


class MyItem(Item):
    """Container for items."""

    url = Field()
    words = Field()


class CrawlingSpider(CrawlSpider):
    """Spider for harvesting words from a URL."""

    name = "crawler"
    
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'crawler.pipelines.CrawlerPipeline': 300,
    #     }
    # }

    def __init__(self, url=None, *args, **kwargs):
        """Initialize a harvest spider."""
        self.url = url
        engine = db_connect()
        create_keyword_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.start_urls = [url]
        self.rules = (Rule(LinkExtractor(allow=("", ),), callback="parse", follow=True),)

    def parse(self, response):
        """Get links from site."""
        # import pdb; pdb.set_trace()
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
        item['words'] = ''
        item['url'] = response.url
        import pdb; pdb.set_trace()
        yield item


def crawl(url):
    """To crawl."""
    settings = get_project_settings()
    settings.url = url
    process = CrawlerProcess(settings)
    process.crawl(CrawlingSpider, url=url)
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

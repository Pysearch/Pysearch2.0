import scrapy
import collections
from itertools import dropwhile
from stop_words import get_stop_words
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

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
    Base.metadata.drop_all(engine)
    print('here in create keyword tables')
    Base.metadata.create_all(engine)

# ********************************END DATABASE******************************
# STARTING_URL = 'https://en.wikipedia.org/wiki/Baseball'
# STARTING_URL = 'https://marc-lj-401.herokuapp.com/'
# STARTING_URL = ''
# STARTING_URL = 'http://www.espn.com/'
NUM_OF_OCCURANCES = 3


class HarvestSpider(scrapy.Spider):
    """Spider for harvesting words from a URL."""

    name = "harvester"

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'harvester.pipelines.HarvesterPipeline': 300,
    #     }
    # }

    def __init__(self, url=None, *args, **kwargs):
        """Initialize a harvest spider."""
        print('66666666666666666666666666666666666666666666')
        self.url = url
        engine = db_connect()
        create_keyword_table(engine)
        self.Session = sessionmaker(bind=engine)

    def start_requests(self):
        """Starting place for request."""
        print('77777777777777777777777777777777777777777777', self.url)
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        """Get words from site."""
        words = []
        headers = []
        title = []
        words_in_title = []
        words_in_headers = []
        stop_words = get_stop_words('english')
        h1_res = response.css('h1::text').extract()
        h2_res = response.css('h2::text').extract()
        h3_res = response.css('h3::text').extract()
        h4_res = response.css('h4::text').extract()
        h5_res = response.css('h5::text').extract()
        h6_res = response.css('h6::text').extract()
        title_res = response.css('title::text').extract()
        p_res = response.css('p::text').extract()

        for each in p_res:
            words.extend(each.split())
        for each in h1_res:
            headers.extend(each.split())
        for each in h2_res:
            headers.extend(each.split())
        for each in h3_res:
            headers.extend(each.split())
        for each in h4_res:
            headers.extend(each.split())
        for each in h5_res:
            headers.extend(each.split())
        for each in h6_res:
            headers.extend(each.split())
        for each in title_res:
            title.extend(each.split())
        words = lower_list(words)
        headers = lower_list(headers)
        title = lower_list(title)
        for word in words:
            if word in headers and word not in stop_words:
                words_in_headers.append(word)
            if word in title and word not in stop_words:
                words_in_title.append(word)
        word_count = collections.Counter(words)
        # head_count = collections.Counter(headers)
        # title_count = collections.Counter(title)
        for key, count in dropwhile(lambda key_count: key_count[1] >= NUM_OF_OCCURANCES, word_count.most_common()):
            del word_count[key]
        for key in list(word_count.keys()):
            if key in stop_words:
                del word_count[key]
        # return word_count

        to_add = []
        session = self.Session()
        for word, count in word_count.items():
            new_keyword = Keyword(keyword=word, keyword_weight=count, title_urls='', header_urls='', body_urls='')
            to_add.append(new_keyword)
            print('888888888888888888888888888888888888888888888')
        try:
            session.add_all(to_add)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return word_count


def harvest(url):
    settings = get_project_settings()
    settings.url = url
    process = CrawlerProcess(settings)
    process.crawl(HarvestSpider, url=url)
    process.start()


def lower_list(list_in):
    """Return a list with all words lowercase."""
    list_out = []
    for each in list_in:
        list_out.append(each.lower())
    return list_out


if __name__ == '__main__':
    import sys
    harvest(sys.argv[1])

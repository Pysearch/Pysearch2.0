"""pipelines.py."""
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from pysearch.models import Keyword, Match


from pysearch.models.meta import Base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'Sera',
    # 'password': 'password',
    'database': 'pysearch'
}

MINIMUM_MATCHES = 5


# DeclarativeBase = declarative_base()


def db_connect():
    """Perform database connection using database settings from settings.py. Returns sqlalchemy engine instance."""
    return create_engine(URL(**DATABASE))


def create_keyword_table(engine):
    """Create Tables."""
    Base.metadata.create_all(engine)


class CrawlerPipeline(object):
    """Crawler pipeline for comparing scraped items with items in the database."""

    def __init__(self):
        """Initialize database connection and sessionmaker. Creates deals table."""
        engine = db_connect()
        create_keyword_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        if spider.name is 'crawler':
            session = self.Session()
            try:
                db_words = session.query(Keyword).all()
                match_words = []
                for word in db_words:
                    if word.keyword in item['words']:
                        match = {
                            'word': word.keyword,
                            'key_weight': word.keyword_weight,
                            'count': item['words'][word.keyword],
                            'url': item['url']
                        }
                        match_words.append(match)
                if len(match_words) > MINIMUM_MATCHES:
                    to_add = []
                    for match in match_words:
                        new_keyword = Match(keyword=match['word'], keyword_weight=match['key_weight'], page_url=match['url'], count=match['count'])
                        to_add.append(new_keyword)
                        print('Pysearch Database Updated...')
                    session.add_all(to_add)
                    session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item

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

import os

# DATABASE = {
#     'drivername': 'postgres',
#     'host': 'localhost',
#     'port': '5432',
#     # 'username': 'midfies',
#     # 'password': 'password',
#     'database': 'pysearch'
# }

MINIMUM_MATCHES = 5


# DeclarativeBase = declarative_base()


def db_connect():
    """Perform database connection using database settings from settings.py. Returns sqlalchemy engine instance."""
    FULL_DB_URL = os.environ["DATABASE_URL"]
    db_type = FULL_DB_URL.split("//")[0][:-1]
    db_user = FULL_DB_URL.split("//")[1].split(":")[0]
    db_host = FULL_DB_URL.split("//")[1].split(":")[1]
    db_port = FULL_DB_URL.split("//")[1].split(":")[2].split("/")[0]
    db_name = db_port = FULL_DB_URL.split("//")[1].split(":")[2].split("/")[1]
    pysearch_db = {
        'drivername': db_type,
        'host': db_host,
        'port': db_port,
        'username': db_user,
        'database': db_name,
    }
    return create_engine(URL(**pysearch_db))


def create_keyword_table(engine):
    """Create Tables."""
    Base.metadata.drop_all(engine)
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

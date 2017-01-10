"""pipelines.py."""
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from pysearch.models import Keyword


# class HarvesterPipeline(object):
#     def process_item(self, item, spider):
#         print("***************************************************************")
#         print(item)
#         print(type(item))
#         print(dir(item))
#         return item

from pysearch.models.meta import Base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'database': 'pysearch'
}


# DeclarativeBase = declarative_base()


def db_connect():
    """Perform database connection using database settings from settings.py. Returns sqlalchemy engine instance."""
    return create_engine(URL(**DATABASE))


def create_keyword_table(engine):
    """Create Tables."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class HarvesterPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database."""

    def __init__(self):
        """Initialize database connection and sessionmaker. Creates deals table."""
        engine = db_connect()
        create_keyword_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        to_add = []
        session = self.Session()
        keyword_dict = dict(item)
        for word, count in keyword_dict.items():
            # print('8888888888888888888888888888')
            # print(word)
            # print(count)
            new_keyword = Keyword(keyword=word, keyword_weight=count, title_urls='', header_urls='', body_urls='')
            to_add.append(new_keyword)
        try:
            session.add_all(to_add)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

"""Keyword Model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class Keyword(Base):
    """Keyword Model. Populated by harvester.
    Keywords from harvested page and their
    number of occurences as keyword weight.
    """

    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(Unicode)
    keyword_weight = Column(Unicode)


class Match(Base):
    """Matches model. Populated by crawler.
    Adding urls to match keywords and the
    number of keywords that occur on those url pages.
    """

    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    keyword = Column(Unicode)
    keyword_weight = Column(Unicode)
    page_url = Column(Unicode)
    count = Column(Integer)


Index('my_index', Keyword.id, unique=True, mysql_length=255)

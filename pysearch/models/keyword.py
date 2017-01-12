"""Keyword Model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base

class Keyword(Base):
    """Keyword Model."""

    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(Unicode)
    keyword_weight = Column(Unicode)
    page_url = Column(Unicode)
    count = Column(Integer)


Index('my_index', Keyword.id, unique=True, mysql_length=255)

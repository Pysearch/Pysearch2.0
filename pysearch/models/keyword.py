from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(Unicode)
    keyword_weight = Column(Unicode)
    title_urls = Column(Unicode)
    header_urls = Column(Unicode)
    body_urls = Column(Unicode)


Index('my_index', Keyword.keyword, unique=True, mysql_length=255)

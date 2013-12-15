from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

Base = declarative_base()


def db_connect():
    """
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    """"""
    Base.metadata.create_all(engine)


class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(Integer, primary_key=True)
    high = Column(Float)
    low = Column(Float)
    avg = Column(Float)
    vol = Column(Float)
    vol_cur = Column(Float)
    last = Column(Float)
    buy = Column(Float)
    sell = Column(Float)
    updated = Column(DateTime)
    server_time = Column(DateTime)

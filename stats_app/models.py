from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
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

    def __repr__(self):
        return "%s - %s" % (self.updated, self.last)


class MiningHistory(Base):
    __tablename__ = "mining_history"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    confirmed_rewards = Column(Float)
    round_estimate = Column(Float)
    total_hashrate = Column(Integer)
    payout_history = Column(Integer)
    round_shares = Column(Integer)
    date_added = Column(DateTime)

    def __repr__(self):
        return "%s - %s" % (self.confirmed_rewards, self.date_added)

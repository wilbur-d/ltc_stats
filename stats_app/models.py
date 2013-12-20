from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref

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


class Pool(Base):
    __tablename__ = "pool"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    def __repr__(self):
        return "%s: %s" % (self.name, self.url)


class MiningHistory(Base):
    __tablename__ = "mining_history"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    confirmed_rewards = Column(Float)
    round_estimate = Column(Float)
    total_hashrate = Column(Integer)
    payout_history = Column(Float)
    round_shares = Column(Integer)
    date_added = Column(DateTime)
    pool_id = Column(Integer, ForeignKey('pool.id'))

    pool = relationship("Pool", backref=backref('mining_histories', order_by=id))

    def __repr__(self):
        return "%s - %s" % (self.confirmed_rewards, self.date_added)


class Trades(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    price_currency = Column(String)
    trade_type = Column(String)  # 'Bid' or 'Ask'
    item = Column(String)  # Currency type, e.g., LTC, BTC, etc.
    price = Column(Float)
    tid = Column(Integer)
    amount = Column(Float)
    date = Column(DateTime)

    def __repr__(self):
        return "%s (%s): %s coins at %s" % (self.date, self.trade_type, self.amount, self.price)

class MinerStatus(Base):
    """ Record the status of the miner
    """
    __tablename__ = "miner_status"

    id = Column(Integer, primary_key=True)
    stratum_active = Column(Boolean)
    difficulty_accepted = Column(Float)
    pool_rejected_percent = Column(Float)
    difficulty_rejected = Column(Float)
    diff1_shares = Column(Integer)
    status =  Column(String)
    proxy_type = Column(String)
    best_share = Column(Integer)
    pool_stale_percent = Column(Float)
    quota = Column(Integer)
    rejected = Column(Integer)
    stratum_URL = Column(String)
    user = Column(String)
    long_poll = Column(String)
    accepted =  Column(Integer)
    proxy = Column(String)
    get_failures = Column(Integer)
    difficulty_stale =  Column(Float)
    url = Column(String)
    discarded = Column(Integer)
    has_stratum = Column(Boolean)
    last_share_time = Column(Integer)
    stale = Column(Integer)
    works = Column(Integer)
    pool = Column(Integer)
    priority = Column(Integer)
    getworks = Column(Integer)
    has_GBT = Column(Boolean)
    last_share_difficulty = Column(Float)
    remote_failures = Column(Integer)

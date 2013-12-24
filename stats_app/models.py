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

class GpuStats(Base):
    __tablename__ = "gpu_stats"
    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime)
    gpu = Column(Integer)
    calls = Column(Integer)
    minimum = Column(Float)
    maximum = Column(Float)
    elapsed = Column(Integer)
    gpu_id = Column(String)
    wait = Column(Float)

class CGMinerPoolStats(Base):
    __tablename__ = "cgminer_pool_stats"
    id = Column(Integer, primary_key=True)
    work_can_roll = Column(Boolean)
    pool_av = Column(Float)
    minimum = Column(Float)
    work_roll_time = Column(Integer)
    work_diff = Column(Float)
    net_bytes_recv = Column(Integer)
    times_recv = Column(Integer)
    times_sent = Column(Integer)
    maximum = Column(Float)
    elapsed = Column(Integer)
    pool_min = Column(Float)
    min_diff = Column(Float)
    work_had_expire = Column(Boolean)
    wait = Column(Float)
    stats = Column(Integer)
    calls = Column(Integer)
    bytes_sent = Column(Integer)
    pool_max = Column(Float)
    max_diff = Column(Float)
    pool_num = Column(String)
    work_had_roll_time = Column(Boolean)
    pool_calls = Column(Integer)
    net_bytes_sent = Column(Integer)
    pool_av = Column(Float)
    bytes_recv = Column(Integer)
    max_diff_count = Column(Integer)
    pool_attempts = Column(Integer)
    pool_wait = Column(Float)
    min_diff_count = Column(Integer)

class MinerStatus(Base):
    """ Record the status of the miner
    """
    __tablename__ = "miner_status"

    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime)
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
    stratum_url = Column(String)
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
    has_gbt = Column(Boolean)
    last_share_difficulty = Column(Float)
    remote_failures = Column(Integer)

class MinerSummary(Base):
    __tablename__ = "miner_summary"
    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime)
    difficulty_accepted = Column(Float)
    pool_rejected_percent = Column(Float)
    found_blocks = Column(Integer)
    difficulty_rejected = Column(Float)
    device_rejected_percent = Column(Float)
    pool_stale_percent = Column(Float)
    work_utility = Column(Float)
    rejected = Column(Integer)
    elapsed = Column(Integer)
    hardware_errors = Column(Integer)
    accepted = Column(Integer)
    network_blocks = Column(Integer)
    local_work = Column(Integer)
    get_failures = Column(Integer)
    difficulty_stale = Column(Float)
    total_mh = Column(Float)
    device_hardware_percent = Column(Float)
    discarded = Column(Integer)
    stale = Column(Integer)
    mhs_av = Column(Float)
    getworks = Column(Integer)
    mhs_5s = Column(Float)
    best_share = Column(Integer)
    remote_failures = Column(Integer)
    utility = Column(Float)

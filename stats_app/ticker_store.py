import logging
import sys
import json

import requests
import arrow

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from cgminer import CGMiner as cgm

from models import Ticker, MiningHistory, Trades, Pool, CGMinerPoolStats, GPUStats, db_connect, create_tables

log = logging.getLogger(__name__)


class BaseStore(object):
    model = None

    def __init__(self, url):
        self.url = url
        engine = db_connect()
        try:
            create_tables(engine)
        except:
            e = sys.exc_info()[0]
            log.error("Unable to create tables. %s" % e)
        self.Session = sessionmaker(bind=engine)

        if not self.model:
            log.warning("BaseStore instantiated without model class variable")
            raise NotImplementedError("Subclasses must set model class!")

    def get_feed(self):
        r = requests.get(self.url)
        return r.json()

    def parse_feed(self, data):
        return data

    def save(self):
        session = self.Session()

        try:
            feed_data = self.get_feed()
        except:
            e = sys.exc_info()[0]
            log.error("Unable to get feed data. %s" % e)
        else:
            feed_dict = self.parse_feed(feed_data)

        stats_obj = self.model(**feed_dict)
        session.add(stats_obj)
        session.commit()
        return stats_obj


class TickerStore(BaseStore):
    model = Ticker

    def parse_feed(self, data):
        ticker = data['ticker']
        ticker['updated'] = arrow.get(ticker['updated']).datetime
        ticker['server_time'] = arrow.get(ticker['server_time']).datetime
        return ticker


class MiningHistoryStore(BaseStore):
    model = MiningHistory

    def __init__(self, pool_api):
        url = pool_api['url']
        super(MiningHistoryStore, self).__init__(url)
        pool_name = pool_api['name']

        self.session = self.Session()
        if not self.session.query(exists().where(Pool.name == pool_name).where(Pool.url == url)).scalar():
            pool = Pool(name=pool_name, url=url)
            self.session.add(pool)
            self.session.commit()
        else:
            pool = self.session.query(Pool).filter(Pool.name == pool_name).filter(Pool.url == url).one()

        self.pool = pool

    def parse_feed(self, data):
        _ = data.pop('workers', None)
        mining_status = data
        mining_status['date_added'] = arrow.utcnow().datetime
        return mining_status

    def save(self):
        try:
            feed_data = self.get_feed()
        except:
            e = sys.exc_info()[0]
            log.error("Unable to get feed data. %s" % e)
        else:
            feed_dict = self.parse_feed(feed_data)

        stats_obj = self.model(**feed_dict)
        stats_obj.pool = self.pool

        self.session.add(stats_obj)
        self.session.commit()

        return stats_obj


class TradeStore(BaseStore):
    """ The trade api returns a list of trades
    like the following:

    {u'price_currency': u'USD',
    u'trade_type': u'bid',
    u'item': u'LTC',
    u'price': 29.57,
    u'tid': 20572079, <-- are the unique over all time?
    u'amount': 1,
    u'date': 1387055215}
    """
    model = Trades

    def save(self):
        """ since we have a list of trades, we have to handle this differently """
        session = self.Session()
        feed_data = self.get_feed()
        for item in feed_data:
            #if session.query(Trades).filter(Trades.tid == item['tid']).count() == 0:
            if not session.query(exists().where(Trades.tid == item['tid'])).scalar():
                feed_dict = item
                feed_dict['date'] = arrow.get(feed_dict['date']).datetime
                stats_obj = self.model(**feed_dict)
                session.add(stats_obj)
                session.commit()
            #return stats_obj # do we need to return this?


class GPUStore(BaseStore):
    model = GpuStats

    def get_feed(self):
        s = cgm(api_ip='192.168.11.99')
        return json.loads(s.command('stats').json())

    def parse_feed(self,data):
        pass

class MinerPoolStore(BaseStore):
    model = CGMinerPoolStats

    def get_feed(self):
        s = cgm(api_ip='192.168.11.99')
        return json.loads(s.command('stats').json())

    def parse_feed(self,data):
        pass

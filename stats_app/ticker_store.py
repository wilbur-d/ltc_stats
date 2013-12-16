import requests
import arrow

from sqlalchemy.orm import sessionmaker

from models import Ticker, MiningHistory, db_connect, create_tables


class BaseStore(object):
    model = None

    def __init__(self, url):
        self.url = url
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

        if not self.model:
            raise NotImplementedError("Subclasses must set model class!")

    def get_feed(self):
        r = requests.get(self.url)
        return r.json()

    def parse_feed(self, data):
        return data

    def save(self):
        session = self.Session()

        feed_data = self.get_feed()
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

    def parse_feed(self, data):
        _ = data.pop('workers', None)
        mining_status = data
        mining_status['date_added'] = arrow.utcnow().datetime
        return mining_status

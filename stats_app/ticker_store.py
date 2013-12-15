import requests
import arrow

from sqlalchemy.orm import sessionmaker

from models import Ticker, db_connect, create_tables


class TickerStore(object):

    def __init__(self, url):
        self.url = url
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def get_ticker(self):
        r = requests.get(self.url)
        return r.json()

    def parse_ticker(self, data):
        ticker = data['ticker']
        ticker['updated'] = arrow.get(ticker['updated']).datetime
        ticker['server_time'] = arrow.get(ticker['server_time']).datetime
        return ticker

    def save_ticker(self):
        session = self.Session()

        ticker_data = self.get_ticker()
        ticker_dict = self.parse_ticker(ticker_data)
        ticker = Ticker(**ticker_dict)

        session.add(ticker)
        session.commit()
        return ticker

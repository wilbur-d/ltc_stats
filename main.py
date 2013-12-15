#! /usr/bin/env python

from stats_app.ticker_store import TickerStore
from stats_app.settings import API_URL


if __name__ == "__main__":
    tstore = TickerStore(API_URL)
    tstore.save_ticker()

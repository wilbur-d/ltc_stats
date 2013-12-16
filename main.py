#! /usr/bin/env python

from stats_app.ticker_store import TickerStore, MiningHistoryStore
from stats_app.settings import API_URL, MINING_API_URL


if __name__ == "__main__":

    tstore = TickerStore(API_URL)
    tstore.save()

    mstore = MiningHistoryStore(MINING_API_URL)
    mstore.save()

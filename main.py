#! /usr/bin/env python

from stats_app.ticker_store import TickerStore, MiningHistoryStore, Tradestore
from stats_app.settings import API_URL, MINING_API_URL, TRADE_API_URL


if __name__ == "__main__":
    tradestore = TradeStore(TRADE_API_URL)
    tradestore.save()

    tstore = TickerStore(API_URL)
    tstore.save()

    # mstore = MiningHistoryStore(MINING_API_URL)
    # mstore.save()

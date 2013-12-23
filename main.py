#! /usr/bin/env python

import logging
import sys

from stats_app.ticker_store import TickerStore, MiningHistoryStore, TradeStore
from stats_app.settings import API_URL, POOLS, TRADE_API_URL, MINER_IP, MINER_PORT

from cgminer import CGMiner

log = logging.getLogger(__name__)


def active_pool_api():
    miner = CGMiner(MINER_IP, MINER_PORT)
    r = miner.command('pools')
    pools = r.dict()['POOLS']
    active = next((p for p in pools if p['Stratum Active'] is True), None)
    active_pool = POOLS[active['URL']]
    active_api = active_pool['url']
    return active_api


if __name__ == "__main__":
    try:
        mstore = MiningHistoryStore(active_pool_api())
        mstore.save()
    except:
        e = sys.exc_info()[0]
        log.error("Unable to save MiningHistory. %s" % e)
        raise

    try:
        tstore = TickerStore(API_URL)
        tstore.save()
    except:
        e = sys.exc_info()[0]
        log.error("Unable to save Ticker. %s" % e)

    try:
        tradestore = TradeStore(TRADE_API_URL)
        tradestore.save()
    except:
        e = sys.exc_info()[0]
        log.error("Unable to save Trade. %s" % e)

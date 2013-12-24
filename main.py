#! /usr/bin/env python

import logging
import sys

from stats_app.ticker_store import TickerStore, MiningHistoryStore, TradeStore, GPUStore, MinerPoolStore, MinerSummaryStore
from stats_app.settings import API_URL, POOLS, TRADE_API_URL, MINER_IP, MINER_PORT

from cgminer import CGMiner

log = logging.getLogger(__name__)


def active_pool():
    miner = CGMiner(MINER_IP, MINER_PORT)
    r = miner.command('pools')
    pools = r.dict()['POOLS']
    active = next((p for p in pools if p['Stratum Active'] is True), None)
    active_pool = POOLS[active['URL']]
    return active_pool


if __name__ == "__main__":
    try:
        mstore = MiningHistoryStore(active_pool())
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

    try:
        gpustore = GPUStore('stats')
        gpustore.save()
    except:
        e = sys.exc_info()[0]
        log.error("Unable to save GPU stats. %s" % e)

    try:
        poolstore = MinerPoolStore('stats')
        poolstore.save()
    except:
        e = sys.exc_info()[0]
        log.error("Unable to save Miner pool stats. %s" % e)

    try:
        minersummary = MinerSummaryStore('summary')
        minersummary.save()
    except:
        e = sys.exc_info()[0]
        log.error("Unable either to acquire or to save Miner Summary stats")

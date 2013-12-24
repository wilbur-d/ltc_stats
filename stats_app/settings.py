import os
import logging

DEBUG = False

# API settings
API_URL = "https://btc-e.com/api/2/ltc_usd/ticker"
TRADE_API_URL = "https://btc-e.com/api/2/ltc_usd/trades"

POOLS = {"stratum+tcp://usa.wemineltc.com:3334": {
    "name": "wemine",
    "url": "https://www.wemineltc.com/api?api_key=YOUR_API_KEY_HERE",
},
    "stratum+tcp://lite.coin-pool.com:3333": {
        "name": "lite.coin-pool.com",
        "url": "http://lite.coin-pool.com/api.php?api_key=YOUR_API_KEY_HERE",
    }
}

MINER_IP = '127.0.0.1'
MINER_PORT = 4028

# Project settings
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, '../ticker.db')

DATABASE = {'drivername': 'sqlite',  # postgresql
            'database': DB_PATH}
            # 'host': '',
            # 'port': '',
            # 'username': '',
            # 'password': ''}

# Logging settings
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "ltc.log")
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

# local settings override
try:
    from local_settings import *
except ImportError, exp:
    pass

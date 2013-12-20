import os
import logging

DEBUG = False

# API settings
API_URL = "https://btc-e.com/api/2/ltc_usd/ticker"

POOLS = {"wemine": {
    "name": "wemine",
    "url": "https://www.wemineltc.com/api?api_key=YOUR_API_KEY_HERE",
},
    "coin-pool": {
        "name": "lite.coin-pool.com",
        "url": "http://lite.coin-pool.com/api.php?api_key=YOUR_API_KEY_HERE",
    }
}

POOL = POOLS['coin-pool']

TRADE_API_URL = "https://btc-e.com/api/2/ltc_usd/trades"

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

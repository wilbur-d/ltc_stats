import os
import logging

# API settings
API_URL = "https://btc-e.com/api/2/ltc_usd/ticker"
MINING_API_URL = ""
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

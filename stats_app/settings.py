API_URL = "https://btc-e.com/api/2/ltc_usd/ticker"
MINING_API_URL = ""

DATABASE = {'drivername': 'sqlite',  # postgresql
            'database': 'ticker.db'}
            # 'host': '',
            # 'port': '',
            # 'username': '',
            # 'password': ''}


try:
    from local_settings import *
except ImportError, exp:
    pass

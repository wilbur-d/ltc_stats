LTC Stats version 0.1
===========================

Setup
-------------------
pip install -r requirements.txt


To Run
-------------------
./main.py


Defaults
-------------------
Database = sqlite db named ticker.db
API = https://btc-e.com/api/2/ltc_usd/ticker


Info
-------------------
Settings are contained in stats_app/settings.py

Example database configuraton for using a postgresql db

DATABASE = {'drivername': 'postgresql',
            'database': 'ticker',
            'host': 'localhost',
            'port': '5432',
            'username': 'postgres',
            'password': 'postgres'}


TODO
-------------------
We're getting some data, let's do something with it...

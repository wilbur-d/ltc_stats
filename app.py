#! /usr/bin/env python

from flask import Flask
from flask import render_template

from sqlalchemy.engine.url import URL

from flask.ext.sqlalchemy import SQLAlchemy

from stats_app.settings import DATABASE

from stats_app.models import Ticker, MiningHistory


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL(**DATABASE)
db = SQLAlchemy(app)


@app.route('/')
def index():
    tickers = db.session.query(Ticker).order_by(Ticker.updated.desc()).all()[:10]
    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added.desc()).all()[:30]
    return render_template('index.html', tickers=tickers, history=history, active="home")


@app.route('/charts')
def charts():
    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added).all()[-30:]
    return render_template('charts.html', history=history, active="charts")


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')

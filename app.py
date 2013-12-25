#! /usr/bin/env python

from flask import Flask, request
from flask import render_template

from sqlalchemy.engine.url import URL

from flask.ext.sqlalchemy import SQLAlchemy

from stats_app.settings import DATABASE, DEBUG

from stats_app.models import Ticker, MiningHistory, Pool, MinerSummary

from stats_app.utils import humanize_minutes, calculate_deltas, average, stdev, chunk_on_interval

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL(**DATABASE)
db = SQLAlchemy(app)


@app.route('/')
def index():
    tickers = db.session.query(Ticker).order_by(Ticker.updated.desc()).all()[:10]
    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added.desc()).all()[:30]
    try:
        pool_worth = "%.2f" % round(tickers[0].last * history[0].confirmed_rewards, 2)
    except:
        pool_worth = "0.0"

    # get latest update
    current_entry = history[0]

    # this try/except is bad. I am a lazy man
    try:
        # get the last entry from the previous pool
        last_change = db.session.query(MiningHistory).order_by(MiningHistory.date_added.desc()).filter(MiningHistory.pool != current_entry.pool)[0]

        # calculate how long we have been on current pool
        timediff = current_entry.date_added - last_change.date_added
        minutes_on_pool = timediff.seconds/60

        time_on_pool = humanize_minutes(minutes_on_pool)
    except:
        time_on_pool = "FOREVER"

    return render_template(
        'index.html',
        tickers=tickers,
        history=history,
        pool_worth=pool_worth,
        active="home",
        current_pool=current_entry.pool,
        time_on_pool=time_on_pool)


@app.route('/charts/')
def charts():
    # get arguments
    records = int(request.args.get('records', 50))
    interval = int(request.args.get('interval', 5))
    pool = request.args.get('pool', None)
    order = request.args.get('order', 'asc')

    # if pool is not set use the most recently mined
    if pool is None:
        h1 = db.session.query(MiningHistory).order_by(MiningHistory.date_added.desc()).first()
        pool = h1.pool.name

    # since we store records in 5 minute intervals
    # we need to pull more records from the db
    # to compensate. They're filtered out in
    # calculate_deltas. This should be improved
    record_multiplier = interval/5

    # Broken logic somewhere so we need to add 1 here
    # probably somewhere in calculate_deltas
    mult_records = records*record_multiplier + 1

    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added).filter(MiningHistory.pool.has(name=pool))

    # get the last *mult_records* number of entries
    history = history[-mult_records:]

    history = chunk_on_interval(history, interval)

    # defaults to asc
    if order == 'desc':
        history.reverse()

    return render_template('charts.html', history=history, active="charts")


@app.route('/stats/')
def stats():
    # get arguments
    records = int(request.args.get('records', 50))
    interval = int(request.args.get('interval', 5))
    pool = request.args.get('pool', None)
    order = request.args.get('order', 'desc')

    # if pool is not set use the most recently mined
    if pool is None:
        h1 = db.session.query(MiningHistory).order_by(MiningHistory.date_added.desc()).first()
        pool = h1.pool.name

    # since we store records in 5 minute intervals
    # we need to pull more records from the db
    # to compensate. They're filtered out in
    # calculate_deltas. This should be improved
    record_multiplier = interval/5

    # Broken logic somewhere so we need to add 1 here
    # probably somewhere in calculate_deltas
    mult_records = records*record_multiplier + 1

    # get our history for the pool
    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added).filter(MiningHistory.pool.has(name=pool))

    # get the last *mult_records* number of entries
    history = history[-mult_records:]

    # calculate deltas
    deltas = calculate_deltas(history, interval)

    if order == 'desc':
        # order defaults to ascending in order to help calculate
        # the deltas. Make it desc
        deltas.reverse()

    # Continuing broken logic from adding 1 to records above
    # makes sure we have at most the actual requested # of records
    deltas = deltas[:records]

    # let's just build this list once
    hdelts = [h.delta for h in deltas]

    # calculate avg delta
    avg_delta = average(hdelts)

    # std dev
    std_dev = stdev(hdelts)

    # set some human readable times
    human_interval = humanize_minutes(interval)

    # get the pools for the drop down selection
    pools = db.session.query(Pool).all()

    return render_template(
        'stats.html',
        active="stats",
        deltas=deltas,
        interval=human_interval,
        pools=pools,
        records=len(deltas),
        active_pool=pool,
        avg_delta=avg_delta,
        std_dev=std_dev,
    )


@app.route('/payouts')
def payouts():
    return render_template('payouts.html', active="payouts")

@app.route('/summary')
def summary():
    summaries = db.session.query(MinerSummary).order_by(MinerSummary.date_added).all()[-10:]
    summaries.reverse()
    return render_template('miner_summary.html', summaries=summaries, active="miner_summary")

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')

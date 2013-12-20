#! /usr/bin/env python

import datetime
import math

from flask import Flask, request
from flask import render_template

from sqlalchemy.engine.url import URL

from flask.ext.sqlalchemy import SQLAlchemy

from stats_app.settings import DATABASE, DEBUG

from stats_app.models import Ticker, MiningHistory, Pool


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL(**DATABASE)
db = SQLAlchemy(app)


def round_time(dt=None, roundTo=60):
    """
    Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)


@app.route('/')
def index():
    tickers = db.session.query(Ticker).order_by(Ticker.updated.desc()).all()[:10]
    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added.desc()).all()[:30]
    try:
        pool_worth = "%.2f" % round(tickers[0].last * history[0].confirmed_rewards, 2)
    except:
        pool_worth = "0.0"
    return render_template('index.html', tickers=tickers, history=history, pool_worth=pool_worth, active="home")


@app.route('/charts/')
def charts():
    history = db.session.query(MiningHistory).order_by(MiningHistory.date_added).all()[-30:]
    return render_template('charts.html', history=history, active="charts")


def calculate_deltas(history, interval):
    deltas = []
    # previous entery; default to the first one
    prev = history[0]
    for h in history:
        # possible broken diff filtering logic somewhere below
        # get time delta of the difference of the two history entries
        # rounded to the nearest minute
        time_diff = round_time(h.date_added) - round_time(prev.date_added)

        # timedelta to minutes
        time_diff = time_diff.total_seconds()/60

        # if the diff is greater than or equal to the requested interval
        if time_diff >= interval:
            # add the payout history to rewards
            current_total_rewards = h.confirmed_rewards + h.payout_history
            prev_total_rewards = prev.confirmed_rewards + prev.payout_history
            # and calculate the delta
            h.delta = current_total_rewards - prev_total_rewards
            deltas.append(h)
            # set current entry to prev
            prev = h
    return deltas


def average(l):
    """
    returns the average value of a list of integers
    """
    return sum(l)/len(l)


def stdev(l):
    """
    return the standard deviation of a list of integers
    """
    avg = average(l)
    variance = map(lambda x: (x - avg)**2, l)
    avg_variance = average(variance)
    return math.sqrt(avg_variance)


def humanize_minutes(mins):
    """
    return a human readable string of time
    from minutes
    """
    if mins >= 60 and mins < 1440:
        # greater than or equal to 1 hour, and less than 1 day, return hours
        human = "%s hour" % (mins/60)
    elif mins >= 1440:
        # greater than or equal to 1 day, return days
        human = "%s day" % (mins/1440)
    else:
        # less than an hour, return the minutes
        human = "%s minute" % mins
    return human


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

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')

import datetime
import math


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


def chunk_on_interval(history, interval, datetime_attr="date_added", round_date=True, round_seconds=60):
    """
    takes a list of objects (history) and an interval
    returns a list objects with a minumum time difference of interval
    optionally rounding to N seconds
    """
    chunks = []
    prev = history[0]
    for h in history:
        # possible broken diff filtering logic somewhere below
        current_datetime = getattr(h, datetime_attr)
        prev_datetime = getattr(prev, datetime_attr)

        # if round round to nearest round_seconds
        if round_date:
            current_datetime = round_time(current_datetime, round_seconds)
            prev_datetime = round_time(prev_datetime, round_seconds)

        # get time delta
        time_diff = current_datetime - prev_datetime

        # timedelta to minutes
        time_diff = time_diff.total_seconds()/60

        # if the diff is greater than or equal to the requested interval
        if time_diff >= interval:
            # add to chunks
            chunks.append(h)
            # set current entry to prev
            prev = h
    # chunks.append(history[-1])
    return chunks


def calculate_deltas(history, interval):
    history = chunk_on_interval(history, interval)

    deltas = []
    prev = history[0]
    for h in history:
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

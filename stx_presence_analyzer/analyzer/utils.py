# -*- coding: utf-8 -*-

def group_by_weekday(items):
    """
    Groups presence entries by weekday.
    """
    result = {i: [] for i in range(7)}
    for date in items:
        start = items[date]['start']
        end = items[date]['end']
        result[date.weekday()].append(interval(start, end))
    return result


def group_times_by_weekday(items):
    """
    Groups times presence entries by weekday.
    """
    result = {i: {'start': [], 'end': []} for i in range(7)}
    for date, times in items.items():
        result[date.weekday()]['start'].append(
            seconds_since_midnight(times['start']))
        result[date.weekday()]['end'].append(
            seconds_since_midnight(times['end']))
    return result


def seconds_since_midnight(time):
    """
    Calculates amount of seconds since midnight.
    """
    return time.hour * 3600 + time.minute * 60 + time.second


def interval(start, end):
    """
    Calculates inverval in seconds between two datetime.time objects.
    """
    return seconds_since_midnight(end) - seconds_since_midnight(start)


def mean(items):
    """
    Calculates arithmetic mean. Returns zero for empty lists.
    """
    return float(sum(items)) / len(items) if len(items) > 0 else 0

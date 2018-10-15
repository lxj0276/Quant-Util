# -*- coding: utf-8 -*-

# 保存全局变量
_global_options = {}


def set_option(key, value):
    _global_options[key] = value


def get_option(key, default=None):
    return _global_options.get(key, default)


# 日历
_calendar = []


def set_calendar(calendar_type):
    import os
    import pandas as pd
    from feature.env import CALENDAR_PATH

    calendar_path = os.path.join(CALENDAR_PATH, calendar_type + '.txt')
    if not os.path.exists(calendar_path):
        raise ValueError('Invalid calendar type: {}'.format(calendar_type))
    with open(calendar_path) as f:
        _calendar = [pd.to_datetime(x.strip()).date() for x in f]


def get_calendar():
    return _calendar

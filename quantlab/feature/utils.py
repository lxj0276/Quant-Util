# -*- coding: utf-8 -*-
import os
import glob
import pickle
import dill
import inspect
import hashlib
import datetime
import time
import numpy as np
import pandas as pd
from pandas.core.tools.datetimes import parse_time_string


def pickle_load(fname):
    with open(fname, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            return pd.Series()
    return data


def pickle_dump(data, fname):
    # create directory automatically
    fpath = os.path.dirname(fname)
    if not os.path.exists(fpath):
        try:
            os.makedirs(fpath)
        except:
            pass
    # save pickle
    f = open(fname, 'wb')
    try:
        pickle.dump(data, f)
    except BaseException:
        f.close()
        os.system('rm {}'.format(fname))
        return False
    else:
        f.close()
    return True


def hash_args(*args, **kwargs):
    string = ''.join(sorted(str(x) for x in args)) + ''.join(sorted(str(x) for x in kwargs.items()))
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def load_source(obj):
    try:
        return inspect.getsource(obj)
    except:
        pass

    try:
        return dill.source.getsource(obj)
    except:
        raise


def func_hash(function):
    try:
        string = load_source(function)
    except:
        string = str(dill.dumps(function)).split('<ipython')[0].split('pyq')[0].split('\\x00\\x00\\x00')
        if len(string)!=1:
            string = string[0:-2]
        string = ''.join(string)
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def find_date_index(series, date):
    for index, time in enumerate(series.index):
        if time>=date:
            return index
    return len(series.index)


def parse_date_str(date_str, tag='begin'):
    date, _, granularity = parse_time_string(str(date_str))
    if tag == 'begin':
        return date
    else:
        offset = pd.DateOffset(**{granularity+'s': 1})
        return date + offset - pd.to_timedelta('1s')


# def resample_day(series, freq, op):

#     freq_num = 0
#     group_index = []
#     dates = series.index.date
#     for i, date in enumerate(dates):
#         if i == len(dates)-1:
#             break
#         if date != dates[i+1]:
#             freq_num += 1
#         if freq_num == freq:
#             group_index.append(date)
#             freq_num = 0
#         else:
#             group_index.append(None)
#     group_index.append(dates[-1])
#     group_index = pd.DatetimeIndex(pd.Series(group_index).bfill())
#     series = series.groupby(group_index).aggregate(op)
#     return series


def resample_minute(series, freq, op):
    series = series.groupby(series.index.ceil(str(freq)+'min')).apply(op)
    return series

def resample_day(series, freq, op):
    base = pd.to_datetime(series.index[0].date())
    group_key = (series.index - base).days // freq
    new_series = series.groupby(group_key).apply(op)
    new_series.index = pd.Series(series.index).groupby(group_key).last()
    new_series.index = new_series.index.normalize()
    return new_series

def resample_week(series, freq, op):
    base = series.index[0] - pd.DateOffset(days=series.index[0].weekday())
    group_key = (series.index - base).days // (7 * freq)
    new_series = series.groupby(group_key).apply(op)
    new_series.index = pd.Series(series.index).groupby(group_key).last()
    new_series.index = new_series.index.normalize()
    return new_series


def resample_month(series, freq, op):
    group_key = series.index.year*100 + (series.index.month - 1) // freq
    new_series = series.groupby(group_key).apply(op)
    new_series.index = pd.Series(series.index).groupby(group_key).last()
    new_series.index = new_series.index.normalize()
    return new_series


def resample_year(series, freq, op):
    group_key = (series.index.year - 1) // freq
    new_series = series.groupby(group_key).apply(op)
    new_series.index = pd.Series(series.index).groupby(group_key).last()
    new_series.index = new_series.index.normalize()
    return new_series


def freq_resample(series, freq, op):
    if series.empty:
        return series
    dic = {
        'm': resample_minute,
        'd': resample_day,
        'W': resample_week,
        'M': resample_month,
        'Y': resample_year,
    }
    freq_unit = freq[-1]
    freq_num = int(freq[:-1])
    assert freq_unit in dic
    return dic[freq_unit](series, freq_num, op)

#
# from .ops import Shift, Rolling
# def batch_shift(feature, shift_list=[0,1,2,3,5,10,15,20]):
#     '''
#     Upper package of shift operator
#     shift the feature by period in shift_list
#     return a list of features
#     '''
#     return [Shift(feature, i) for i in shift_list]
#
# def batch_rolling(feature, func, rolling_list=[1,3,5,10]):
#     '''
#     Upper package of rolling operator
#     rolling the feature by func with period in rolling_list
#     return a list of features
#     '''
#     return [Rolling(feature, i, func) for i in rolling_list]
#


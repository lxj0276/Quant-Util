# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


_ANNUAL_FACTORS = {
    'd': 244,
    'D': 244,
    'W': 52,
    'w': 52,
    'M': 12,
    'y': 1,
    'Y': 1,
}
_RISK_FREE_RETURN = 0.03

def risk_analysis(returns, freq='1d'):
    """calculate annual return of return sequence.

    Parameters
    ----------
    returns : np.array
        return sequence
    freq : str
        return frequency

    Returns
    ----------
    total_return : float
        total return
    annual_return : float
        annual return
    sharpe_ratio : float
        sharpe ratio
    drawdown : tuple
        max drawdown
    """
    returns = np.array(returns)
    try:
        factor = _ANNUAL_FACTORS[freq[-1]] / int(freq[:-1])
    except:
        raise ValueError("frequency cannot be {}, possible values: {}".format(
        freq, ", ".join(_ANNUAL_FACTORS.keys())))
    # total return
    total_return = np.expm1(np.cumsum(np.log1p(returns)))
    # annual return
    annual_return = (1 + total_return[-1]) ** (factor / len(returns)) - 1
    # sharpe ratio
    risk_free_by_freq = _RISK_FREE_RETURN / factor
    avg_excess_return = np.mean(returns - risk_free_by_freq)
    std_excess_return = np.std(returns - risk_free_by_freq - avg_excess_return, ddof=1)
    sharpe_ratio = np.sqrt(factor) * avg_excess_return / std_excess_return
    # max drawdown
    end = np.argmax(np.maximum.accumulate(total_return) - total_return)
    begin = np.argmax(total_return[:end]) if end > 0 else 0
    drawdown = (total_return[end] - total_return[begin]) / (total_return[begin] + 1)
    return total_return, annual_return, sharpe_ratio, (begin, end, drawdown)


def train_test_split(dataset, train_span=48, valid_span=3, test_span=3, unit='M'):
    """将数据按照滑动时间窗口切分

    Parameters
    ----------
    dataset : Dataset
        数据集
    train_span : int
        训练周期长度
    valid_span : int
        验证周期长度
    test_span : int
        测试周期长度
    unit : str
        周期单位，D-日/W-周/M-月/Y-年

    Returns
    ----------
    dtrain : Dataset
        训练集
    dvalid : Dataset
        验证集
    dtest : Dataset
        测试集
    """

    begin_time = dataset.index.min()
    end_time   = dataset.index.max()
    unit_mapping = {
        'D': 'days',
        'W': 'weeks',
        'M': 'months',
        'Y': 'years',
    }
    unit = unit.upper()
    if unit not in unit_mapping:
        raise ValueError('unit {} is not valid, possible values are {}'.format(
            unit, ', '.join(unit_mapping.keys())
        ))
    test_time  = begin_time + pd.DateOffset(**{unit_mapping[unit]: train_span + valid_span + test_span})
    if test_time > end_time:
        raise ValueError('train({})+valid({})+test({}) exceed maximum time range {:%Y/%m/%d}~{:%Y/%m/%d}'.format(
            train_span, valid_span, test_span, begin_time, end_time
        ))
    while test_time < end_time:
        train_time = begin_time + pd.DateOffset(**{unit_mapping[unit]: train_span})
        valid_time = train_time + pd.DateOffset(**{unit_mapping[unit]: valid_span})
        test_time  = valid_time + pd.DateOffset(**{unit_mapping[unit]:  test_span})
        dtrain = dataset[(dataset.index>=begin_time)&(dataset.index<train_time)]
        dvalid = dataset[(dataset.index>=train_time)&(dataset.index<valid_time)]
        dtest  = dataset[(dataset.index>=valid_time)&(dataset.index<test_time)]
        yield dtrain, dvalid, dtest
        begin_time += pd.DateOffset(**{unit_mapping[unit]: valid_span or test_span})


def is_tradetme(tme):
    return 900 <= tme.hour*100 + tme.minute < 1500 or \
    2100 <= tme.hour*100 + tme.minute < 2300 # 交易时间
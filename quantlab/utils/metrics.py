# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def auc_score(pct_change, scores):
    """calculate auc score according to percent change and predict scores.

    Parameters
    ----------
    pct_change : percent change of price
    scores     : prediction scores

    Returns
    ----------
    auc : auc score
    """
    tmp = pd.DataFrame()
    tmp['pct_change'] = pct_change
    tmp['scores'] = scores
    log_return = tmp.sort_values('scores', ascending=False)['pct_change'].map(np.log1p).cumsum()
    oracle_log_return = tmp.sort_values('pct_change', ascending=False)['pct_change'].map(np.log1p).cumsum()
    baseline = (oracle_log_return.iloc[0] + oracle_log_return.iloc[-1]) * len(tmp) * 0.5
    auc = (np.sum(log_return) - baseline) / (np.sum(oracle_log_return) - baseline)
    return auc


def max_drawdown(returns):
    """calculate max drawdown of return sequence.

    Parameters
    ----------
    returns : daily/weekly/monthly/annually return sequence

    Returns
    ----------
    begin    : maximum drawdown begin
    end      : maximum drawdown end
    drawdown : maximum drawdown

    Examples
    ----------
    """
    returns = np.array(returns)
    nav = np.expm1(np.cumsum(np.log1p(returns)))
    end = np.argmax(np.maximum.accumulate(nav) - nav)
    begin = np.argmax(nav[:end])
    drawdown = (nav[end] - nav[begin]) / (nav[begin] + 1)
    return begin, end, drawdown

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

def sharpe(returns, freq='1d'):
    """calculate sharpe ratio of return sequence.

    Parameters
    ----------
    returns : return sequence
    freq    : return frequency

    Returns
    ----------
    sharpe ratio

    Examples
    ----------
    """
    returns = np.array(returns)
    try:
        factor = _ANNUAL_FACTORS[freq[-1]] / int(freq[:-1])
    except:
        raise ValueError("frequency cannot be {}, possible values: {}".format(
	    freq, ", ".join(_ANNUAL_FACTORS.keys())))
    risk_free_by_freq = _RISK_FREE_RETURN / factor
    avg_excess_return = np.mean(returns - risk_free_by_freq)
    std_excess_return  = np.std(returns - risk_free_by_freq - avg_excess_return, ddof=1)
    return np.sqrt(factor) * avg_excess_return / std_excess_return

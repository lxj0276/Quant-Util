# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from quantlab.utils.metrics import sharpe


def weighted_logloss(data):
    feature = data.feature
    weight  = data.weight
    def scorer(model):
        scores = model.predict(feature)
        score = np.average(label*np.log(scores)+(1-label)*np.log(1-scores), weights=weight)
        return score
    return scorer

def weighted_accuracy(data):
    feature = data.feature
    weight  = data.weight
    def scorer(model):
        scores = np.round(model.predict(feature))
        score = np.average(label==scores, weights=weight)
        return score
    return scorer

def weighted_precision(data):
    feature = data.feature
    weight  = data.weight
    def scorer(model):
        scores = np.round(model.predict(feature))
        score = np.average(label[scores==1], weights=weight)
        return score
    return scorer

def logloss(data):
    feature = data.feature
    def scorer(model):
        scores = model.predict(feature)
        score = np.average(label*np.log(scores)+(1-label)*np.log(1-scores))
        return score
    return scorer

def accuracy(data):
    feature = data.feature
    def scorer(model):
        scores = np.round(model.predict(feature))
        score = np.average(label==scores)
        return score
    return scorer

def precision(data):
    feature = data.feature
    def scorer(model):
        scores = np.round(model.predict(feature))
        score = np.average(label[scores==1])
        return score
    return scorer

def sharpe_ratio(data, topk=10):
    datetime = data.datetime
    pct_change = data.pct_change
    freq = data.freq
    def scorer(model):
        scores = model.predict(data.feature)
        pred = pd.DataFrame({
            'datetime': datetime,
            'pct_change': pct_change,
            'scores': scores
        })
        returns  = pred.groupby('datetime').apply(
            lambda x: x.sort_values('scores', ascending=False).head(topk)['pct_change'].mean() - 0.002
        ).shift(1).fillna(0)
        _sharpe_ratio = sharpe(returns, freq=freq)
        return _sharpe_ratio
    return scorer

def total_return(data, topk=10):
    datetime = data.datetime
    pct_change = data.pct_change
    def scorer(model):
        scores = model.predict(data.feature)
        pred = pd.DataFrame({
            'datetime': datetime,
            'pct_change': pct_change,
            'scores': scores
        })
        returns  = pred.groupby('datetime').apply(
            lambda x: x.sort_values('scores', ascending=False).head(topk)['pct_change'].mean() - 0.002
        ).shift(1).fillna(0)
        _total_return = returns.map(np.log1p).cumsum().map(np.expm1)[-1]
        return _total_return
    return scorer

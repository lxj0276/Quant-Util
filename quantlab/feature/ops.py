# -*- coding: utf-8 -*-
import copy
import numpy as np
import pandas as pd
from operator import add, sub, mul, truediv
from scipy.stats import percentileofscore, linregress
from numpy.lib.type_check import isnan
from numpy.core.fromnumeric import all as np_all, sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum, nanmax, nanmin
from .base import Feature, OperatorFeature
from .utils import freq_resample, func_hash
from ._libs.rolling import rolling_slope, rolling_rsquare


class Shift(OperatorFeature):
    """Shift operator can shift a time series by desired number of periods.

    Parameters
    ----------
    feature : <Feature>, feature instance
    period  : <int>, can be positive (past data) or negative (future data)

    Returns
    ----------
    series  : <pandas.Series>, shifted time series

    Examples
    ----------
    """
    def __init__(self, feature, period):
        self.feature = feature
        self.period  = period

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.period)

    def _load_feature(self, instrument_id, time_range):
        return self.feature.load(instrument_id, time_range).shift(self.period)


class Mask(OperatorFeature):
    """Mask operator can override default feature call mechanism.

    Parameters
    ----------
    feature       : <Feature>, feature instance
    instrument_id : <str>, default None, instrument_id to override
    time_range    : <TimeRange>, default None, time_range to override

    Returns
    ----------
    series        : <pandas.Series>, masked time series

    Examples
    ----------
    """
    def __init__(self, feature, instrument_id=None):
        self.feature       = feature
        self.instrument_id = instrument_id

    def __str__(self):
        return '{}({}, {})'.format(self.name, self.feature, self.instrument_id)

    def _load_feature(self, instrument_id, time_range):
        return self.feature.load(self.instrument_id or instrument_id, time_range)

    
class MultiResample(OperatorFeature):
    """MultiResample operator can turn a set of features into a single feature with different granularity. func will receive an input with type pd.DataFrame

    Parameters
    ----------
    features  : list of <Feature>, feature instances
    freq      : <string>, resample frequency
    func      : <function>, function to apply

    Returns
    ----------
    series   : <pandas.Series>, converted feature

    Examples
    ----------
    """
    def __init__(self, features, freq, func=lambda x:x.iloc[-1]):
        self.features = features
        self.freq     = freq
        self.func     = func # default use last

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.features, self.freq, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        series = []
        for feature in self.features:
            series.append(feature.load(instrument_id, time_range))
        df = pd.concat(series, axis=1)
        series = freq_resample(df, self.freq, self.func)
        return series

    
class Resample(OperatorFeature):
    """Resample operator can turn a minute feature into a daily feature.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    func     : <function>, function to apply

    Returns
    ----------
    series   : <pandas.Series>, converted feature

    Examples
    ----------
    """
    def __init__(self, feature, freq, func=lambda x:x.iloc[-1]):
        self.feature = feature
        self.freq    = freq
        self.func    = func # default use last

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.freq, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        series = freq_resample(series, self.freq, self.func)
        return series


class Rloc(Resample):
    """Resample locate operator can locate certain minute.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq, time):
        self.feature = feature
        self.freq    = freq
        self.time    = pd.to_datetime(time).time()

        func = lambda x: (x[x.index.time == self.time].values[-1:] or [np.nan])[0] # TODO: improve speed
        super(Rloc, self).__init__(self.feature, self.freq, func)

    def __str__(self):
        return '{}({}, {}, {:%H:%M:%S})'.format(
            self.name, self.feature, self.freq, self.time)


class Rmax(Resample):
    """Resample max operator can locate certain minute.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rmax, self).__init__(
            feature, freq,
            lambda x: np.nan if np_all(isnan(x)) else nanmax(x)
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Rmin(Resample):
    """Resample min operator can locate certain minute.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rmin, self).__init__(
            feature, freq,
            lambda x: np.nan if np_all(isnan(x)) else nanmin(x)
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Rfirst(Resample):
    """Resample first operator can locate certain minute.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rfirst, self).__init__(
            feature, freq,
            lambda x: x.loc[x.first_valid_index() or x.index[0]]
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Rlast(Resample):
    """Resample last operator can locate certain minute.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rlast, self).__init__(
            feature, freq,
            lambda x: x.loc[x.last_valid_index() or x.index[-1]]
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Rsum(Resample):
    """Resample sum operator sum series in resample period.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rsum, self).__init__(
            feature, freq,
            lambda x: np.nan if np_all(isnan(x)) else nansum(x)
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Rmean(Resample):
    """Resample mean operator calculate series mean in resample period.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rmean, self).__init__(
            feature, freq,
            lambda x: np.nan if np_all(isnan(x)) else nanmean(x)
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Rstd(Resample):
    """Resample std operator calculate series std in resample period.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    freq     : <string>, resample frequency
    time     : <string>, timestamp

    Returns
    ----------
    series   : <pandas.Series>, resampled series

    Examples
    ----------
    """
    def __init__(self, feature, freq):
        super(Rstd, self).__init__(
            feature, freq,
            lambda x: isnan if np_sum(~isnan(x)) < 2 else nanstd(x, ddof=1)
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.freq)


class Map(OperatorFeature):
    """Map operator can calculate element-wise

    Parameters
    ----------
    feature  : <Feature>, feature instance
    func     : <function>, operation function

    Returns
    ----------
    series   : <pandas.Series>, operated time series

    Examples
    ----------
    """
    def __init__(self, feature, func, name='Default'):
        self.feature = feature
        self.func    = func
        self.fname   = name

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.fname, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        return self.feature.load(instrument_id, time_range).map(self.func)


class Scale(Map):
    """Scale operator can scale data element-wise

    Parameters
    ----------
    feature  : <Feature>, feature instance
    multiply : <float>, scale num

    Returns
    ----------
    series   : <pandas.Series>, operated time series

    Examples
    ----------
    """
    def __init__(self, feature, multiply):
        super(Scale, self).__init__(
            feature, lambda x: x*multiply
        )
        self.multiply = multiply

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.multiply)


class Multi_rolling(OperatorFeature):
    """Multi_rolling operator can map given operation on rolling windows of a list of pd.series. These series are concated first and then rolling as dataframe. The variable of parameter "func" will be a dataframe

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size for rolling
    func     : <function>, operation function

    Returns
    ----------
    series   : <pandas.Series>, operated time series

    Examples
    ----------
    """
    def __init__(self, features, window, func):
        self.features = features
        self.window   = window
        self.func     = func

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.features, self.window, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        series = []
        for feature in self.features:
            series.append(feature.load(instrument_id, time_range))
        df = pd.concat(series, axis=1)
        if len(df) < self.window:
            series = pd.Series()
        else:
            series = pd.Series(
                [self.func(df.iloc[i:i+self.window]) for i in range(len(df)-self.window+1)],
                index=df.index[self.window-1:len(df)+1]
            )
        series = pd.concat([pd.Series(np.nan, index=df.index[:self.window-1]), series])
        return series


class Rolling(OperatorFeature):
    """Rolling operator can map given operation on rolling windows of time series.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size for rolling
    func     : <function>, operation function

    Returns
    ----------
    series   : <pandas.Series>, operated time series

    Examples
    ----------
    """
    def __init__(self, feature, window, func):
        self.feature = feature
        self.window  = window
        self.func    = func

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.window, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).apply(self.func)
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series


class Max(Rolling):
    """Max operator will calculate max value on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling max series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).max()
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series
        

class Min(Rolling):
    """Min operator will calculate min value on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling min series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).min()
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series
        

class MA(Rolling):
    """MA operator will calculate mean value on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling mean series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).mean()
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series


class Sum(Rolling):
    """Sum operator will calculate mean value on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling sum series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).sum()
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series


class Vola(Rolling):
    """Vola operator will calculate std value on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling std series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).std()
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series


class Quantile(Rolling):
    """Quantile operator will calculate quantile value on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling
    qscore   : <float>, range [0, 1]

    Returns
    ----------
    series   : <pandas.Series>, rolling quantile series

    Examples
    ----------
    """
    def __init__(self, feature, window, qscore):
        self.feature = feature
        self.window  = window
        self.qscore  = qscore

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.window, self.qscore)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.rolling(self.window, min_periods=1).quantile(self.qscore)
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series

    
class Pos(Rolling):
    """Pos operator will calculate percentile of score on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling percentile series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        super(Pos, self).__init__(
            feature, window,
            lambda x: np.nan if isnan(x[-1]) else
            percentileofscore(x[~isnan(x)], x[-1])*0.01
        )

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)


class Slope(Rolling):
    """Slope operator will calculate slope of series on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling slope series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        series = pd.Series(rolling_slope(series.values, self.window), index=series.index)
        series.iloc[:self.window-1] = np.nan
        return series

    
class Rsquare(Rolling):
    """Rsquare operator will calculate r2 of series on rolling window.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size foll rolling

    Returns
    ----------
    series   : <pandas.Series>, rolling r2 series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        series = pd.Series(rolling_rsquare(series.values, self.window), index=series.index)
        series.iloc[:self.window-1] = np.nan
        return series


class EMA(OperatorFeature):
    """EMA operator will calculate the Exponentially-weighted moving average of time series.

    Parameters
    ----------
    feature  : <Feature>, feature instance
    window   : <int>, window size for ewma, also called "span" in pandas. [See: http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.ewma.html]

    Returns
    ----------
    series   : <pandas.Series>, operated time series

    Examples
    ----------
    """
    def __init__(self, feature, window):
        self.feature = feature
        self.window  = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range)
        isnull = series.isnull()
        series = series.ewm(span=self.window).mean()
        series[isnull] = np.nan
        series.iloc[:self.window-1] = np.nan
        return series


class Operator(OperatorFeature):
    """Operator will accept two feature and return operator product.

    Parameters
    ----------
    feature_left  : <Feature>, left  feature instance
    feature_right : <Feature>, right feature instance
    operator      : <operator>, operator function

    Returns
    ----------
    series        : <pandas.Series>, operator produced time series

    Examples
    ----------
    """
    def __init__(self, feature_left, feature_right, operator):
        self.feature_left  = feature_left
        self.feature_right = feature_right
        self.operator      = operator

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature_left, self.feature_right)

    def _load_feature(self, instrument_id, time_range):
        try:
            assert isinstance(self.feature_left, Feature) or isinstance(self.feature_right, Feature)
        except:
            raise TypeError('at least one of two arguments is Feature instance')
        if isinstance(self.feature_left, Feature):
            series_left = self.feature_left.load(instrument_id, time_range)
        else:
            series_left = self.feature_left
        if isinstance(self.feature_right, Feature):
            series_right = self.feature_right.load(instrument_id, time_range)
        else:
            series_right = self.feature_right
        series = self.operator(series_left, series_right)
        return series


class Mul(Operator):
    """Mul Operator will accept two feature and return multiply product.

    Parameters
    ----------
    feature_left  : <Feature>, left  feature instance
    feature_right : <Feature>, right feature instance

    Returns
    ----------
    series        : <pandas.Series>, multiply produced time series

    Examples
    ----------
    """
    def __init__(self, feature_left, feature_right):
        super(Mul, self).__init__(feature_left, feature_right, mul)


class Div(Operator):
    """Div Operator will accept two feature and return divide product.

    Parameters
    ----------
    feature_left  : <Feature>, left  feature instance
    feature_right : <Feature>, right feature instance

    Returns
    ----------
    series        : <pandas.Series>, divide produced time series

    Examples
    ----------
    """
    def __init__(self, feature_left, feature_right):
        super(Div, self).__init__(feature_left, feature_right, truediv)


class Add(Operator):
    """Add Operator will accept two feature and return add product.

    Parameters
    ----------
    feature_left  : <Feature>, left  feature instance
    feature_right : <Feature>, right feature instance

    Returns
    ----------
    series        : <pandas.Series>, added produced time series

    Examples
    ----------
    """
    def __init__(self, feature_left, feature_right):
        super(Add, self).__init__(feature_left, feature_right, add)


class Sub(Operator):
    """Sub Operator will accept two feature and return sub product.

    Parameters
    ----------
    feature_left  : <Feature>, left  feature instance
    feature_right : <Feature>, right feature instance

    Returns
    ----------
    series        : <pandas.Series>, subed produced time series

    Examples
    ----------
    """
    def __init__(self, feature_left, feature_right):
        super(Sub, self).__init__(feature_left, feature_right, sub)


class Minute_Map_Day(OperatorFeature):
    def __init__(self, feature, func, name='Default'):
        self.feature = feature
        self.func = func
        self.fname = name

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.fname, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        raise NotImplemented
        return self.feature.load(instrument_id, time_range).groupby('date').apply(self.func)


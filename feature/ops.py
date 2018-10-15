# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from feature._libs.rolling import rolling_slope, rolling_rsquare
from feature.base import Feature, OperatorFeature
from feature.cons import FREQUANCE_DAY, FREQUANCE_MINUTE,FREQUANCE_TICK
from feature.utils import freq_resample, func_hash, series_frequance
from numpy.core.fromnumeric import all as np_all, sum as np_sum
from numpy.lib.nanfunctions import nanmean, nanstd, nansum, nanmax, nanmin, nanmedian
from numpy.lib.type_check import isnan
from operator import add, sub, mul, truediv, and_, invert
from pandas._libs.algos import rank_2d_float64
from scipy.stats import percentileofscore


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
        self.period = period

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.period)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.period)).shift(self.period)
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
        return series


# ------------------------to be overwrite------------------------------------------------------------------
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
        self.feature = feature
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

    def __init__(self, features, freq, func=lambda x: x.iloc[-1]):
        self.features = features
        self.freq = freq
        self.func = func  # default use last

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


# ---------------------------------------------------------

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

    def __init__(self, feature, freq, func=lambda x: x.iloc[-1]):
        self.feature = feature
        self.freq = freq
        self.func = func  # default use last

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.freq, func_hash(self.func))

    def _load_feature(self, instrument_ids, time_range):
        series = self.feature.load(instrument_ids, time_range)
        freq = series_frequance(series)
        cols = series.columns
        series.index = pd.to_datetime(series.index.map(lambda x: str(x)))
        result = freq_resample(series, self.freq, self.func)

        if freq == FREQUANCE_DAY:
            result.index = result.index.strftime('%Y%m%d')
        elif freq == FREQUANCE_MINUTE:
            result.index = result.index.strftime('%Y%m%d%H%M')
        elif freq==FREQUANCE_TICK:
            result.index =result.index.strftime('%Y%m%d%H%M%S')
        else:
            raise NotImplemented;

        result.index = result.index.map(int)
        result.columns = cols
        return result


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
        self.freq = freq
        self.time = pd.to_datetime(time).time()

        func = lambda x: (x[x.index.time == self.time].values[-1:] or [np.nan])[0]  # TODO: improve speed
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
            lambda x: pd.Series(nanmax(x, axis=0))
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
            lambda x: pd.Series(nanmin(x, axis=0))
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
            lambda x: pd.Series(nansum(x, axis=0))
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
            lambda x: pd.Series(nanmean(x, axis=0))
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
            lambda x: pd.Series(nanstd(x, axis=0))
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
        self.func = func
        self.fname = name

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.fname, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        return self.feature.load(instrument_id, time_range).applymap(self.func)


class V_Map_FutureData(Map):
    ##use no futuredata map you should go to rolling
    def _load_feature(self, instrument_id, time_range):
        return self.feature.load(instrument_id, time_range).apply(self.func)


class H_Map(Map):
    def _load_feature(self, instrument_id, time_range):
        # apply func to all data in one time point

        return self.feature.load(instrument_id, time_range).apply(lambda x:pd.Series(self.func(x.values),index=x.index), axis=1)


class V_Norm_FutureData(V_Map_FutureData):
    ##use no futuredata map you should go to rolling
    def __init__(self, feature):
        super(V_Norm_FutureData, self).__init__(feature, lambda x: (x - nanmean(x)) / nanstd(x))


class H_Norm(H_Map):
    def __init__(self, feature):
        super(H_Norm, self).__init__(feature, lambda x: (x - nanmean(x)) / nanstd(x))


class H_Norm_Median(H_Map):
    def __init__(self, feature):
        super(H_Norm_Median, self).__init__(feature, lambda x: (x - nanmedian(x)) / nanstd(x))


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
            feature, lambda x: x * multiply
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
        self.window = window
        self.func = func

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.features, self.window, func_hash(self.func))

    def _load_feature(self, instrument_ids, time_range):
        result = pd.DataFrame()
        for col in instrument_ids:
            series = []
            for feature in self.features:
                series.append(feature.load(instrument_ids, time_range)[col])
            df = pd.concat(series, axis=1)
            if len(df) < self.window:
                series = pd.Series()
            else:
                series = pd.Series(
                    [self.func(df.iloc[i:i + self.window]) for i in range(len(df) - self.window + 1)],
                    index=df.index[self.window - 1:len(df) + 1]
                )
            series = pd.concat([pd.Series(np.nan, index=df.index[:self.window - 1]), series])
            result[col] = series
        return result


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
        self.window = window
        self.func = func

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.window, func_hash(self.func))

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window, min_periods=min(2, self.window)).apply(self.func)
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window, min_periods=1).max()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window, min_periods=1).min()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window, min_periods=1).mean()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
        return series



class MA_IGNORE_ZERO(Rolling):
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.replace(0,np.nan).rolling(self.window, min_periods=1).mean()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
        return series

class MA_skipna(Rolling):
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        for col in series.columns:
            series[col]=series[col].dropna().rolling(self.window,min_periods=1).mean().reindex(series.index)
        #series = series.rolling(self.window, min_periods=1).mean()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
        return series

class MEDIAN(Rolling):
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window, min_periods=1).median()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window).sum()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window, min_periods=1).std()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window
        self.qscore = qscore

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.window, self.qscore)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.rolling(self.window).quantile(self.qscore)
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
            percentileofscore(x[~isnan(x)], x[-1]) * 0.01)

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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        for col in series.columns:
            series[col] = pd.Series(rolling_slope(series[col].values, self.window), index=series.index)
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        for col in series.columns:
            series[col] = pd.Series(rolling_rsquare(series[col].values, self.window), index=series.index)
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.window = window

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.window)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(self.window))
        series = series.ewm(span=self.window).mean()
        if series_frequance(series) == FREQUANCE_DAY:
            series = series.loc[time_range.begin_time:time_range.end_time - 1]
        elif series_frequance(series) == FREQUANCE_MINUTE:
            series = series.loc[time_range.begin_time * 10000:time_range.end_time * 10000]
        elif series_frequance(series) == FREQUANCE_TICK:
            series = series.loc[time_range.begin_time :time_range.end_time]
        else:
            raise NotImplemented
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
        self.feature_left = feature_left
        self.feature_right = feature_right
        self.operator = operator

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
        try:
            series = self.operator(series_left, series_right)
        except Exception as e:
            print(self.operator)
            print(series_left)
            print(series_right)
            raise (e)
        return series


class Orthogonalization(Operator):
    def __init__(self, feature_left, feature_right):
        super(Orthogonalization, self).__init__(feature_left, feature_right, Orthogonalization.orth)

    @staticmethod
    def orth(feature_left, feature_right):
        new_feature = pd.DataFrame(index=feature_left.index)
        for col in feature_left.columns:
            rho = feature_left[col].corr(feature_right[col])
            new_feature[col] = feature_left[col] - rho * np.sqrt(feature_left[col].var() / feature_right[col].var()) * \
                                                   feature_right[col]
        return new_feature


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


class And(Operator):
    def __init__(self, feature_left, feature_right):
        self.feature_left = feature_left
        self.feature_right = feature_right

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature_left, self.feature_right)

    def _load_feature(self, instrument_id, time_range):
        try:
            assert isinstance(self.feature_left, Feature) or isinstance(self.feature_right, Feature)
        except:
            raise TypeError('at least one of two arguments is Feature instance')
        if isinstance(self.feature_left, Feature):
            series_left = self.feature_left.load(instrument_id, time_range).astype(bool)
        else:
            series_left = self.feature_left.astype(bool)
        if isinstance(self.feature_right, Feature):
            series_right = self.feature_right.load(instrument_id, time_range).astype(bool)
        else:
            series_right = self.feature_right.astype(bool)
        series = series_left & series_right
        return series


class Astype(Map):
    def __init__(self, feature, thetype):
        self.thetype = thetype
        self.feature = feature

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.thetype)

    def _load_feature(self, instrument_ids, time_range):
        return self.feature.load(instrument_ids, time_range).astype(self.thetype)


class Not(Map):
    def __init__(self, feature, name='Default'):
        super(Not, self).__init__(feature, lambda x: not (x), name)


class Minute_Map_Day(OperatorFeature):
    """
    map minute to day data

    """

    def __init__(self, feature, func, name='Default'):
        self.feature = feature
        self.func = func
        self.fname = name

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.fname, func_hash(self.func))

    def _load_feature(self, instrument_ids, time_range):
        df = self.feature.load(instrument_ids, time_range)
        return df.groupby(lambda x: x // 10000).apply(self.func)


class Round(OperatorFeature):
    def __init__(self, feature, n):
        self.feature = feature
        self.n = n

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.n)

    def _load_feature(self, instrument_ids, time_range):
        df = self.feature.load(instrument_ids, time_range)
        return df.round(self.n)


class Ranking(OperatorFeature):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return '{}({})'.format(
            self.name, self.feature)

    def _load_feature(self, instrument_ids, time_range):
        df = self.feature.load(instrument_ids, time_range)
        rank_np = rank_2d_float64(df, axis=1)
        return pd.DataFrame(rank_np, index=df.index, columns=df.columns)


class Minute_Map(OperatorFeature):
    def __init__(self, feature, func, name='Default'):
        self.feature = feature
        self.func = func
        self.fname = name

    def __str__(self):
        return '{}({}, {}, {})'.format(
            self.name, self.feature, self.fname, func_hash(self.func))

    def _load_feature(self, instrument_ids, time_range):
        df = self.feature.load(instrument_ids, time_range)
        return df.groupby(lambda x: x // 10000, as_index=False).apply(self.func)


class Minute_Daily_Norm(Minute_Map):
    def __init__(self, feature, name='Default'):
        super(Minute_Daily_Norm, self).__init__(feature, lambda x: (x - nanmean(x)) / nanstd(x), name)

    def __str__(self):
        return '{}({})'.format(
            self.name, self.feature)


class Operator_MD(OperatorFeature):
    """Operator work between minute feature and daily feature"""

    def __init__(self, min_feature, day_feature, operator):
        self.min_feature = min_feature
        self.day_feature = day_feature
        self.operator = operator

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.min_feature, self.day_feature)

    def _load_feature(self, instrument_id, time_range):
        min_feature = self.min_feature.load(instrument_id, time_range)
        day_feature = self.day_feature.load(instrument_id, time_range)
        min_idx = min_feature.index
        min_feature.index //= 10000
        try:
            series = self.operator(min_feature, day_feature)
        except Exception as e:
            print(self.operator)
            print(series_left)
            print(series_right)
            raise (e)
        series.index = min_idx
        return series


class Mul_MD(Operator_MD):
    """Mul_MD Operator will accept two feature and return multiply product.

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

    def __init__(self, min_feature, day_feature):
        super(Mul_MD, self).__init__(min_feature, day_feature, mul)


class Div_MD(Operator_MD):
    """Div_MD Operator will accept two feature and return divide product.

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

    def __init__(self, min_feature, day_feature):
        super(Div_MD, self).__init__(min_feature, day_feature, truediv)


class Add_MD(Operator_MD):
    """Add_MD Operator will accept two feature and return add product.

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

    def __init__(self, min_feature, day_feature):
        super(Add_MD, self).__init__(min_feature, day_feature, add)


class Sub_MD(Operator_MD):
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

    def __init__(self, min_feature, day_feature):
        super(Sub_MD, self).__init__(min_feature, day_feature, sub)


# ---------下面是仅对基本面因子的操作符 @author llx--------------------
# 以下OPS继承自PersistentFeature 的原因是，以下操作普遍比较耗时，使用PersistentFeature可以进行缓存
from feature.base import PersistentFeature


class Shift_Fundamental(PersistentFeature):
    """
    获取Shift期间的基本面数据，例如当期是三季报，shift（1）获取半年报，shift（4）获取去年三季报，
    以此类推

    """

    def __init__(self, feature, period):
        self.feature = feature
        self.period = period

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.period)

    def _create_feature(self, instrument_ids, time_range):
        from feature.zoo.Financial_Period import Financial_Period
        financial_period = Financial_Period().load(instrument_ids, time_range.shift(self.period * 150))
        series = self.feature.load(instrument_ids, time_range.shift(self.period * 150))
        for col in financial_period.columns:
            df = pd.concat([financial_period[col], series[col]], axis=1)
            df.columns = ['financial_period', self.feature.get_name()]
            series[col] = df.drop_duplicates().shift(self.period).reindex(series.index).fillna(method='ffill')[
                self.feature.get_name()]
        series = series.loc[time_range.begin_time:time_range.end_time - 1]
        return series


class Single_Period(PersistentFeature):
    """
    获取单季的财务数据，注意，这个operator只能对 利润表，现金流量表等净额表示的指标使用，不能对
    资产负债表等表示总额的指标使用
    """

    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return '{}({})'.format(
            self.name, self.feature)

    def _create_feature(self, instrument_ids, time_range):
        from feature.zoo.Financial_Period import Financial_Period
        financial_period = Financial_Period().load(instrument_ids, time_range.shift(150))
        series = self.feature.load(instrument_ids, time_range.shift(150))
        series_shift = series.copy()
        for col in financial_period.columns:
            df = pd.concat([financial_period[col], series[col]], axis=1)
            df.columns = ['financial_period', self.feature.get_name()]
            series_shift[col] = df.drop_duplicates().shift(1).reindex(series.index).fillna(method='ffill')[
                self.feature.get_name()]
        series = series.loc[time_range.begin_time:time_range.end_time - 1]
        series_shift = series_shift.loc[time_range.begin_time:time_range.end_time - 1]
        financial_period = financial_period.loc[time_range.begin_time:time_range.end_time - 1]
        # 将非一季度报表的数据减去上一个季度的数据
        result = pd.DataFrame(
            np.where(financial_period - 10 * (financial_period // 10) == 1, series, series - series_shift),
            columns=series.columns, index=series.index)
        return result


class TTM(PersistentFeature):
    """
    计算过去四个季度滚动的指标，也就是所谓的TTM指标

    """

    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return '{}({})'.format(
            self.name, self.feature)

    def _create_feature(self, instrument_ids, time_range):
        F1 = Add(Single_Period(self.feature), Shift_Fundamental(Single_Period(self.feature), 1))
        F2 = Add(F1, Shift_Fundamental(Single_Period(self.feature), 2))
        F3 = Add(F2, Shift_Fundamental(Single_Period(self.feature), 3))
        return F3.load(instrument_ids, time_range)


class Increase_Rate(PersistentFeature):
    """
    计算过去财务指标的增长率

    """

    def __init__(self, feature,period):
        self.feature = feature
        self.period=period

    def __str__(self):
        return '{}({},{})'.format(
            self.name, self.feature,self.period)

    def _create_feature(self, instrument_ids, time_range):
        F0=self.feature
        F1=Shift_Fundamental(self.feature,self.period)
        F2=Sub(Div(F0,F1),1)
        return F2.load(instrument_ids, time_range)




if __name__ == '__main__':
    Div(Mul(Close_Daily(), ), Add(
        Single_Period(Net_Profit()) + Single_Period(Net_Profit(), 1) + Single_Period(Net_Profit(), 2) + Single_Period(
            Net_Profit(), 3)))

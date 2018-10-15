from quantlab.feature import *
from quantlab.feature.ops import *
import numpy as np
from scipy.stats import linregress


class Leo1_Daily(NonPersistentFeature):

    description = '线性回归（x=价格涨跌幅绝对值，y=交易量，60日）得到r^2，用来衡量有多少追涨杀跌的人, 表征了这只股票的动量大小'
    formular = 'linregress(change, vol).r^2'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        change = Map(Shift(ChangeRate_Daily(), 1), lambda x: abs(x))
        vol = Map(Div(Vol_Daily(), Shift(Vol_Daily(), 1)), lambda x: x-1)
        leo1 = Multi_rolling([change, vol], 60, lambda x: linregress(x.dropna()).rvalue**2 if len(x.dropna())>2 else np.nan)
        return leo1.load(instrument_id, time_range)

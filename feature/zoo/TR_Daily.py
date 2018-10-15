from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.Low_Daily import Low_Daily

from .TR import TR


class TR_Daily(PersistentFeature):
    description = '真实振幅，常使用其MA14或MA28判断盘整、振荡和单边趋势'
    formula = 'TR=max(|今日振幅|， |昨天收盘-今日最高价|，|昨天收盘-今日最低价|)'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        high = High_Daily()
        low = Low_Daily()
        return TR(close, high, low).load(instrument_id, time_range)

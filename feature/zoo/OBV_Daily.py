from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.Low_Daily import Low_Daily
from feature.zoo.Vol_Daily import Vol_Daily

from .OBV import OBV


class OBV_Daily(PersistentFeature):
    description = '((收盘价-最低价)-(最高价-收盘价)) / (最高价-最低价) * V'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        low = Low_Daily()
        high = High_Daily()
        volume = Vol_Daily()
        return OBV(close, high, low, volume).load(instrument_id, time_range)

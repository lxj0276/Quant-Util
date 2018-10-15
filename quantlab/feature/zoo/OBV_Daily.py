from quantlab.feature import *
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

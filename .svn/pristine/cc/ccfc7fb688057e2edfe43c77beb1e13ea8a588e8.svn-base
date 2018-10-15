from feature.base import PersistentFeature
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily

from .Alpha import Alpha


class AlphaHS300_Daily(PersistentFeature):
    description = '个股关于沪深300的Alpha'
    formula = 'linregress(个股，沪深300)的截距'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Alpha(ChangeRate_Daily(), 'CN_IDX_SH000300', 70).load(instrument_id, time_range)

from feature.base import PersistentFeature
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily

from .Beta import Beta


class BetaHS300_Daily(PersistentFeature):
    description = '个股关于沪深300的beta'
    formula = 'linregress(个股，沪深300)的斜率'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return Beta(ChangeRate_Daily(), 'CN_IDX_SH000300', 70).load(instrument_id, time_range)

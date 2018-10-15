from feature.base import NonPersistentFeature
from feature.ops import *
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily


class Kurtosis_Daily(NonPersistentFeature):
    description = '个股历史22日收益率的峰度'
    formula = ' Kurtosis = E[(x-Ex)^4/Var(x)^2]-3 '
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        def get_kurtosis(x):
            neu_x = ((x - nanmean(x)) / nanstd(x)) ** 4
            return nanmean(neu_x) - 3

        kurtosis = Rolling(ChangeRate_Daily(), 22, get_kurtosis)
        return kurtosis.load(instrument_id, time_range)

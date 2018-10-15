from feature.base import NonPersistentFeature
from feature.ops import *
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily


class Skewness_Daily(NonPersistentFeature):
    description = '个股历史22日收益率的偏度'
    formula = 'Skewness = E[(R)^3], R=(r-mu)/sigma '
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        def get_skewness(x):
            neu_x = ((x - nanmean(x)) / nanstd(x)) ** 3
            return nanmean(neu_x)

        skewness = Rolling(ChangeRate_Daily(), 22, get_skewness)
        return skewness.load(instrument_id, time_range)

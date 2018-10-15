from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_G_NetProfit3YAvg(PersistentFeature):
    description = '3 年净利润增长率的平均值'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

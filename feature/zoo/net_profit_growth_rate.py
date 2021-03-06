from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Net_profit_growth_rate(PersistentFeature):
    description = '净利润增长率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

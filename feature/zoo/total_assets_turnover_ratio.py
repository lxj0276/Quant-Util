from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Total_assets_turnover_ratio(PersistentFeature):
    description = '总资产周转率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

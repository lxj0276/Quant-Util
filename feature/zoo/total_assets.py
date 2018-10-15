from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Total_assets(PersistentFeature):
    description = '总资产'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

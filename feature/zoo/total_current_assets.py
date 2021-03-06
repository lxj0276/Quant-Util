from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Total_current_assets(PersistentFeature):
    description = '流动资产合计'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

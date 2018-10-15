from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Total_current_liability(PersistentFeature):
    description = '流动负债合计'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

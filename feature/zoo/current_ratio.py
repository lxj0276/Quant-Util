from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Current_ratio(PersistentFeature):
    description = '流动比率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Inventory(PersistentFeature):
    description = '存货'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

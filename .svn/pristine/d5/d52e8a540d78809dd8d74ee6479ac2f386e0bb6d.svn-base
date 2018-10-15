from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class High_Min(PersistentFeature):
    description = 'minute highest price feature'

    granularity = 'minute'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Vol_Min(PersistentFeature):
    description = 'minute volume feature'

    granularity = 'minute'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

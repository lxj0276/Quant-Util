from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Money_Min(PersistentFeature):
    description = 'minute money feature'

    granularity = 'minute'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

from feature.base import PersistentFeature

from feature.error import *


class Close_Min(PersistentFeature):
    description = 'minute close price feature'

    granularity = 'minute'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

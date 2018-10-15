from feature.base import PersistentFeature

from feature.error import *


class Close_Tick(PersistentFeature):
    description = 'tick close price feature'

    granularity = 'tick'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

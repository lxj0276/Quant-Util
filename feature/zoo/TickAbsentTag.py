from feature.base import PersistentFeature

from feature.error import *

class Tick_Absent(PersistentFeature):
    description = 'indicate whether data is absent if absent ->value=0'

    granularity = 'tick'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

from quantlab.feature import PersistentFeature
from quantlab.feature.error import OriginalFeatureError


class Vol_Daily(PersistentFeature):

    description = 'daily volume feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

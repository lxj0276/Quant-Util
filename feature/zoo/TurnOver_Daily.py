from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class TurnOver_Daily(PersistentFeature):
    description = 'daily turnover rate'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

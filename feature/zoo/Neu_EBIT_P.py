from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_EBIT_P(PersistentFeature):
    description = 'EBIT/P=息税前盈利/市值'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

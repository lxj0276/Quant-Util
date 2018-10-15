from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_P_EBIT(PersistentFeature):
    description = 'P/EBIT=市值/息税折旧前盈利'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

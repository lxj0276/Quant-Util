from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_CF_P(PersistentFeature):
    description = 'CF_P＝经营现金流量净额/市值'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

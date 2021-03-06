from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Operating_margin(PersistentFeature):
    description = '营运利润率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

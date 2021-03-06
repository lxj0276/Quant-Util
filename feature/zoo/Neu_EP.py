from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_EP(PersistentFeature):
    description = 'EP=归属母公司股东净利润/市值'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Total_liabilities(PersistentFeature):
    description = '负债合计'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

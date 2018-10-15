from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Cost_of_sales(PersistentFeature):
    description = '销售费用'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

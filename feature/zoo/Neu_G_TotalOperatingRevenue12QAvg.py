from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_G_TotalOperatingRevenue12QAvg(PersistentFeature):
    description = '过去 12 个季度营业总收入平均年增长率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

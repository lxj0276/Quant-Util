from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Neu_G_NetCashFlow(PersistentFeature):
    description = '净现金流增长率 = (最近一年净现金流 - 前一期净现金流)/abs(前一期净现金流)'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

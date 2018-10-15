from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Accounts_receivable_turnover_ratio(PersistentFeature):
    description = '应收帐款周转率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

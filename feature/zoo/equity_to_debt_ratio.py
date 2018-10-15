from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Equity_to_debt_ratio(PersistentFeature):
    description = '权益负债比率'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Snowball_deal(PersistentFeature):
    description = '某只股票的雪球累计交易分享数'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        raise OriginalFeatureError('Can not create original features')

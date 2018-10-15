from feature.base import PersistentFeature
from feature.zoo.Close_Daily import Close_Daily

from .TRMA import TRMA


class TRMA_Daily(PersistentFeature):
    description = '中长线指标，是TRIX的20日MA'
    formula = 'TR是close的三重EMA，TRIX=(TR/前日TR-1)*100，TRMA=MA(TRIX, 20)'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        trma = TRMA(close, 12, 20)
        return trma.load(instrument_id, time_range)

from quantlab.feature import *
from .BBI import BBI

class BBI_Daily(PersistentFeature):

    description = '多空头指标，股价在BBI上为多头市场，BBI下为空头市场，由下至上穿越BBI买入，由上至下穿越BBI卖出'
    formular = 'BBI=(MA3+MA6+MA12+MA24)/4'
    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        close = Close_Daily()
        bbi = BBI(close, m=3, n=6, k=12, l=24)
        return bbi.load(instrument_id, time_range)/4

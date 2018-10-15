from quantlab.feature import *
from quantlab.feature.ops import *


class Turnover_Full_At_AM10(PersistentFeature):

    description = 'turnover_full at 10:00'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range,):
        money = Rloc(Sum(Money_Min(), 30), freq='1d', time='10:00:00')
        lc = Shift(Money_Daily(),1)
        return Mul(Div(money, lc), TurnOver_Full_Daily()).load(instrument_id, time_range)

from quantlab.feature import *
from quantlab.feature.ops import *


class ReferencePrice_Daily(PersistentFeature):
    description = '（广发证券）Grinblatt(2005)提出的个股参考价格，广发证券针对A股进行了改进，以日换手率加权的日成交均价'
    formula = '过去100天的日换手率加权的日成交均价'
    granularity = 'day'
    
    def _create_feature(self, instrument_id, time_range):
        def reference_price(data):
            price = data.iloc[:, 0]
            turn = data.iloc[:, 1]
            temp_turn = (1-turn.iloc[::-1]).cumprod().shift(1).fillna(1).iloc[::-1] * turn
            return (temp_turn*price).sum()/temp_turn.sum()
    
        price = Close_Daily() # 应该是成交均价，用收盘价代替
        turn  = TurnOver_Daily()
        RP    = Multi_rolling([price, turn], 100, reference_price)
        return RP.load(instrument_id,time_range)

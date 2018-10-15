from feature.base import PersistentFeature

from feature.error import OriginalFeatureError

from feature.zoo.Total_Shares import Total_Shares
from feature.zoo.net_profit import Net_Profit
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.Recovery_Factor import Recovery_Factor

from feature.ops import *

class Neu_PE(PersistentFeature):
    description = 'PE＝市值/归属母公司股东净利润,TTM'

    def _create_feature(self, instrument_id, time_range):
        market_value=Mul(Div(Close_Daily(),Recovery_Factor()),Total_Shares())
        profit=TTM(Net_Profit())
        pe=Div(market_value,profit)
        return pe.load(instrument_id, time_range)

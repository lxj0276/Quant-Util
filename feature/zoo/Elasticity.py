from feature.base import PersistentFeature
from feature.ops import *

from feature.zoo.Close_Min import Close_Min
from feature.zoo.Open_Min import Open_Min
from feature.zoo.Vol_Min import Vol_Min

class Elasticity(PersistentFeature):
    description="股价的弹性系数，单位资金打入导致的股价变化"

    granularity = 'day'

    def _create_feature(self, instrument_ids, time_range):
        clo=Rlast(Close_Min(),'5m')
        opn=Rfirst(Open_Min(),'5m')
        vol=Rsum(Vol_Min(),'5m')
        rtn=Sub(Div(clo,opn),1)
        abs_rtn=Map(rtn,abs)
        elasticity_min=Div(abs_rtn,vol)
        elasticity_day=Minute_Map_Day(elasticity_min,lambda x:x.sum())
        return elasticity_day.load(instrument_ids, time_range)

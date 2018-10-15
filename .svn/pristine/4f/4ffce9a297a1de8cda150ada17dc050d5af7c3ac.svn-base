from feature.base import PersistentFeature
import pandas as pd
from engine.utils import get_calendar
class evaluator(PersistentFeature):
    def __init__(self,metric):
        self.metric=metric

    def _create_feature(self,strategys,start_time,end_time):
        trade_calendar=get_calendar(start_time,end_time)
        strategys_name=list(map(lambda x: type(x).__name__ + x.name if x.name is not None else '', strategys))
        df=pd.DataFrame(index=trade_calendar,columns=strategys_name)
        for strategy in strategys:
            for trade_date in trade_calendar:
                df.loc[trade_date,type(strategy).__name__ + strategy.name if strategy.name is not None else '']=self.metric.evaluate(strategy.generate_proposal(get_calendar(start_time,trade_date+1)))
        return df

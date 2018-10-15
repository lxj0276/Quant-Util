from feature.base import PersistentFeature

from feature.error import OriginalFeatureError


class Onmarket_Time(PersistentFeature):
    description = '已上市天数，此feature 与tushare 耦合'

    granularity = 'day'

    def _create_feature(self, instrument_ids, time_range):
        import tushare as ts
        import pandas as pd
        from engine.utils import get_calendar
        basic=ts.get_stock_basics()['timeToMarket']
        basic=basic[basic!=0]
        basic.index=basic.index.map(lambda x:'CN_STK_SH'+x if x[0]=='6' else 'CN_STK_SZ'+x)
        basic=basic[basic.index.isin(instrument_ids)]
        basic=basic.astype(str)
        series=pd.DataFrame(index=get_calendar(time_range.begin_time,time_range.end_time),columns=instrument_ids)
        fill_data=list(series.index.map(str))
        for col in series.columns:
            series[col]=fill_data
        for col in series.columns:
            if col in basic.index:
                series[col]=pd.to_datetime(series[col])-pd.to_datetime(basic.at[col])
            else:
                series[col]=pd.NaT

        series=series.applymap(lambda x:x.days)
        return  series


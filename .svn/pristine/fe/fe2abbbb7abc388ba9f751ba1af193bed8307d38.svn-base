import pandas as pd
from feature.base import PersistentFeature
from feature.zoo import Close_Min,Vol_Min
from feature.ops import *
class DBX(PersistentFeature):
    index_path = '/data/production/AStock_history/Index_MinK_by_Index/'

    def __init__(self, index_id):
        self.index_id = index_id

    def _create_feature(self, instrument_ids, time_range):
        import pandas as pd
        normed_vol_min = Minute_Daily_Norm(Vol_Min()).load(instrument_ids, time_range)
        return_min = Rolling(Close_Min(), 2, lambda x: x[1] / x[0] - 1).load(instrument_ids, time_range).fillna(0)
        index_path = '/data/production/AStock_history/Index_MinK_by_Index/'
        df = pd.read_csv(index_path + self.index_id + '.csv')
        df.index = df['date'] * 10000 + df['time'].map(lambda x: int(x.replace(':', '')))
        df = df[['close', 'vol']]
        df['thereturn'] = df['close'].rolling(window=2).apply(lambda x: x[1] / x[0] - 1).fillna(0)
        df = df.loc[time_range.begin_time * 10000:time_range.end_time * 10000]

        alpha_return = return_min.sub(df['thereturn'], axis=0)
        return (alpha_return * normed_vol_min).groupby(lambda x: x // 10000).apply(lambda x: x.sum())

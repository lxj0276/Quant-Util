from feature import *
from feature.ops import *
import pandas as pd
import numpy as  np
# from redis_cache.utils import flush#清除缓存数据库
# flush()
instrument_ids=list_instrument_ids(instrument_type='STK')[:10]
time_range=TimeRange(20170301,20180101)
Total_assets().load(instrument_ids,time_range)
Total_Shares().load(instrument_ids,time_range)
Neu_PE().load(instrument_ids,time_range)
start_time=20170301
end_time=20170501
#
# clo=Close_Daily()
# opn=Open_Daily()
# r=Return_NDay_Label(1)
# Feature_Importance_Base([clo,opn],r).load(instrument_ids,time_range)
# df=load_dataset(instrument_ids,[clo,opn,r],time_range,return_xarray=False)
# Rsum(Close_Min(),'5m').load(instrument_ids,time_range)
# Rmean(Close_Min(),'5m').load(instrument_ids,time_range)
# Rfirst(Close_Min(),'5m').load(instrument_ids,time_range)
elasticity_day= Elasticity()
elasticity_day.load(instrument_ids,time_range)
df=Close_Min().load(instrument_ids,time_range)
df['datetime']=df.index
df=df.groupby(lambda x:x//5,as_index=False).apply(lambda x:x.iloc[0])
df['datetime']=df['datetime'].astype(int)
df=df.set_index('datetime')
df=df.iloc[:20]
df.index//5
df=Financial_Period().load(instrument_ids,time_range)

Rlast(Close_Min(),'5m').load(instrument_ids,time_range)
opn=Rfirst(Open_Min(),'5m')
vol=Rsum(Vol_Min(),'5m')
rtn=Sub(Div(clo,opn),1)
abs_rtn=Map(rtn,abs)
elasticity_min=Div(abs_rtn,vol)
elasticity_day=Minute_Map_Day(elasticity_min,lambda x:x.sum())

df=pd.DataFrame(np.random.randn(5,5))
pd.Series().rank
import scipy
scipy.stats.rankdata


clo=Close_Daily()
rank_clo=Ranking(clo)
rank_clo.load(instrument_ids,time_range)
from feature.feature_analyse import *
#
#
# clo=Close_Min()
# clo1=Shift(Close_Min(),1)
# # f=Shift(clo,1)
# # r=Resample(clo,'7d')
# # r1=Rmax(clo,'7d')
# #
# # Min(clo,window=2).load(instrument_ids,timerange)
# # Max(clo,window=2).load(instrument_ids,timerange)
# # Quantile(clo,window=2,qscore=0.5).load(instrument_ids,timerange)
# Rsquare(clo,window=3).load(instrument_ids,time_range)
# df1=clo.load(instrument_ids,time_range)
# df2=clo1.load(instrument_ids,time_range)
# #
#
# ADX_Daily().load(instrument_ids,timerange)
# AroonUp_Daily().load(instrument_ids,timerange)
#
#
# load_dataset(instrument_ids, timerange, [Close_Daily(),Rsquare(clo,window=3).set_name('SB')])
#
#
# clo.load(instrument_ids,timerange)
#
#
# df=r.load(instrument_ids,timerange)
# r1.load(instrument_ids,timerange)
# clo.load(instrument_ids,timerange)
# ChangeRate_Daily().load(instrument_ids,timerange)
#
# df1=Orthogonalization(Min(clo,window=2),Rsquare(clo,window=3)).load(instrument_ids,timerange)
# df2=Rsquare(clo,window=3).load(instrument_ids,timerange)
#
# for col in df1.columns:
#     print(df1[col].corr(df2[col]))
# df.corr()
#

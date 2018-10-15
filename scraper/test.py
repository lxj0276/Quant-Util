from tqdm import tqdm
from feature import *
import logging
from scraper.juchao_spider import juchao_spider
instrument_ids=list_instrument_ids(instrument_type='STK')
instrument_ids=list(map(lambda x:x[-6:],instrument_ids))
s=juchao_spider()

lrbs=[]
lrb_failed=[]
for code in tqdm(instrument_ids):
    try:
        inner_df=s.get_records(code,'lrb',"2010","2018",use_proxy=True)
    except Exception as e:
        print(code)
        print(e)
        lrb_failed.append(code)
        continue
    lrbs.append(inner_df)
lrb=pd.concat(lrbs,axis=0)

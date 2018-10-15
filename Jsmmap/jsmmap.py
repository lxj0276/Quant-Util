import Jsmmap.Jsmmap as jp
import numpy as np
from Jsmmap.cons import *
import pandas as pd



def get_data_single_field(stockId,start_tick,end_tick,field_name):
    return jp.readFields(os.path.join(MMAP_FILE_PATH,stockId),start_tick,end_tick,field_name)


def get_data_single_field_COLUMN(stockId,start_tick,end_tick,field_name):
    return jp.readFields_column(os.path.join(MMAP_COLUMN_FILE_PATH,stockId),start_tick,end_tick,field_name)


def get_data_muti_field(stockId,start_tick,end_tick,field_names):
    arrys=jp.readMultiFields(os.path.join(MMAP_FILE_PATH,stockId),start_tick,end_tick," ".join(field_names))
    return np.stack(arrys,axis=1)

def get_data_muti_field_withlist(stockId,start_tick,end_tick,field_names):
    arrys=jp.readMultiFields(os.path.join(MMAP_FILE_PATH,stockId),start_tick,end_tick," ".join(field_names))
    return arrys


def get_tick_trade_data(instrumentids,startTick,endTick,field_name):
    if len(set(instrumentids).intersection(set(STOCK_UNIVERSE)))!=len(instrumentids):
        raise ValueError("contain invalid stockId or dupucates stockId")
    data=get_data_muti_field_withlist(instrumentids[0],startTick,endTick,["时间","trading_date"])
    timstramp=data[1].astype(np.int64)*1000000+data[0]
    df=pd.DataFrame(np.zeros((len(timstramp),len(instrumentids))),index=timstramp,columns=instrumentids)

    for instrumentId in instrumentids:
        df[instrumentId]=get_data_single_field_COLUMN(instrumentId,startTick,endTick,field_name)
    return df



if __name__=="__main__":
    import glob
    from tqdm import tqdm
    filenames=glob.glob(CSV_DATA_PATH+'/*')
    filename=filenames[0]
    for filename in tqdm(filenames):
        jp.csvToMmapFile_COLUMN(filename,os.path.join(MMAP_COLUMN_FILE_PATH,filename.split('/')[-1][:-4]))
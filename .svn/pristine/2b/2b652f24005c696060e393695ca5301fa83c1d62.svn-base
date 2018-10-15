import pandas as pd
import pymongo
from mongoapi.env import GLOBAL_MONGO_CONN

def cxdict_2_df(cx_dict):
    result = []
    for field, d1 in cx_dict.items():
        for instrument_id, d2 in d1.items():
            for thedate, data in d2.items():
                result.append((field, instrument_id, thedate, data))
    return pd.DataFrame(result, columns=['field', 'instrument_id', 'thedate', 'data'])

def collection_rename(db_name, collection_name, new_name):
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    DATA_COLLECTION = DATA_DB[collection_name]
    DATA_COLLECTION.rename(new_name)

def set_search_index(db_name, collection_name, index):
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    DATA_COLLECTION = DATA_DB[collection_name]
    DATA_COLLECTION.create_index(index)


def initialize_collection(db_name, collection_name):
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    DATA_DB.create_collection(collection_name)


def df_to_mongo(df, index_fields, db_name, collection_name):
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    DATA_COLLECTION = DATA_DB[collection_name]
    df_insert = df[index_fields]
    insert_records = []
    for i in range(len(df_insert)):
        insert_records.append(df_insert.iloc[i].to_dict())
    DATA_COLLECTION.insert(insert_records)

def df_to_mongo(df,db_name,collection_name,if_exists='error',indexes=None):
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    try:
        DATA_COL=DATA_DB[collection_name]
    except:
        DATA_DB.create_collection(collection_name)
        DATA_COL = DATA_DB[collection_name]
    if DATA_COL.count()==0:
        pass

    else:
        if if_exists=='error':
            raise ValueError("插入的collection 已经存在，并有documents")

        elif if_exists=='append':
            pass

        elif if_exists=='ignore':
            DATA_COL.delete_many({})

        else :raise NotImplemented
    DATA_COL.insert_many(df.to_dict('records'))
    if not indexes is None:
        for index in indexes:
            DATA_COL.ensure_index(index)



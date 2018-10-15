from utils import *
import pymongo
from mongoapi.env import GLOBAL_MONGO_CONN
import pandas as pd

def index_demo():
    index_list = ['code', 'date']
    db_name = 'db_index'
    collection_name_list = ['IndexByMinute']
    for collection_name in collection_name_list:
        for index_name in index_list:
            set_search_index(db_name=db_name, collection_name=collection_name, index=index_name)
            print('{} {} {}'.format(db_name, collection_name, index_name))

def fundamental_rename():
    db_name = 'fundamental'
    collection_name_list = ['balance_sheet', 'cashflow_sheet', 'profit_sheet']
    for collection_name in collection_name_list:
        collection_rename(db_name, collection_name, collection_name+'_full')

def fundamental_init_collention():
    db_name = 'fundamental'
    collection_name_list = ['balance_sheet', 'cashflow_sheet', 'profit_sheet']
    for collection_name in collection_name_list:
        initialize_collection(db_name, collection_name)


def fundamental_insert(db_name, collection_name, new_collection_name):
    print("{} {} {}".format(db_name, collection_name, new_collection_name))
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    DATA_COLLECTION = DATA_DB[collection_name]
    data = list(DATA_COLLECTION.find({'F003V': '合并本期'}))
    DATA_NEW_COLLECTION = DATA_DB[new_collection_name]
    DATA_NEW_COLLECTION.insert_many(data)

def fundamental_insert_V2(db_name, collection_name, new_collection_name):
    DATA_DB = GLOBAL_MONGO_CONN[db_name]
    DATA_COLLECTION = DATA_DB[collection_name]
    data = list(DATA_COLLECTION.find())
    df = pd.DataFrame(data)
    df = df[df.F003V=='合并本期']
    DATA_NEW_COLLECTION = DATA_DB[new_collection_name]
    DATA_NEW_COLLECTION.insert_many(df.to_dict('records'))


def fundamental_index(index_name):
    db_name = 'fundamental'
    collection_name_list = ['balance_sheet', 'cashflow_sheet', 'profit_sheet']
    for col_name in collection_name_list:
        collection_name = col_name
        print('{} {} {}'.format(db_name, collection_name, index_name))
        set_search_index(db_name, collection_name, index_name)


def fundamental_demo():
    db_name = 'fundamental'
    collection_name_list = ['balance_sheet', 'cashflow_sheet', 'profit_sheet']
    collection_name  = 'balance_sheet_full'
    for col_name in collection_name_list:
        col_new_name = col_name
        col_old_name = col_name+'_full'
        fundamental_insert(db_name, col_old_name, col_new_name)

if __name__ == '__main__':
    index_demo()

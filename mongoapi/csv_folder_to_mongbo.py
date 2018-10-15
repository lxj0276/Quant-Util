# lian
# exmaple of stock record in mongodb
import csv
import os

import pymongo


class stock_record:
    def __init__(self, code, date, open, high, low, close, vol, money, turnover, turnover_full, rate):
        self.code = code
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.vol = vol
        self.money = money
        self.turnover = turnover
        self.turnover_full = turnover_full
        self.rate = rate


class MongoDB_Cnector:
    def __init__(self, host='localhost', port=27017, db_name='db_stock', col_name='stocks'):
        self.conn = pymongo.MongoClient(host=host, port=port)
        self.db = self.conn[db_name]
        self.stock = self.db[col_name]

    def write_record(self, type):
        '''
        :param type: stock record
        :return: None
        '''
        self.stock.insert(type.__dict__)

    def write_file(self, filename):
        # write one csv file into the mongoapi
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                one = stock_record(
                    code=row['code'],
                    date=int(row['date']),
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    vol=float(row['vol']),
                    money=float(row['money']),
                    turnover=float(row['turnover']),
                    turnover_full=float(row['turnover_full']),
                    rate=float(row['rate'])
                )
                self.write_record(one)

    def write_folder(self, folder_path):
        files = os.listdir(folder_path)
        for fi in files:
            fi_d = os.path.join(folder_path, fi)
            if os.path.isfile(fi_d):
                if '.csv' in str(fi_d):
                    self.write_file(str(fi_d))


if __name__ == '__main__':
    mongoconn = MongoDB_Cnector()
    folder_path = r'C:\Users\jingjingxu\Desktop\Stock_DayK_by_Stock'
    mongoconn.write_folder(folder_path)

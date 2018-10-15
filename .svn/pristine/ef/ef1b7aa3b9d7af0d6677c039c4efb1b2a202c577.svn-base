import csv

import pymongo


class stock_record:
    def __init__(self, code, date, open, high, low, close, volume):
        self.code = code
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume=volume

def write_dict(type,col):
    col.insert(type.__dict__)


# useage example
if __name__ == "__main__":

    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.db_stock
    stock = db.stocks
    file_name = 'SH600000.csv'
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            one = stock_record(
                code=row['code'],
                date=row['date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume']
            )
            write_dict(one)
    print(db.stocks.count())

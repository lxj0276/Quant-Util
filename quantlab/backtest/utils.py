# -*- coding: utf-8 -*-
import os
import time
import csv
import numpy as np
import pandas as pd
from . import Tick
from . import Minute
import datetime


def get_index(list, time):
    for i,current_time in enumerate(list):
        if i>len(list)-2:
            return -1
        elif time ==current_time:
            return i
        elif current_time<=time and list[i+1]>time:
            return i
    return -1


def max_drop_down(serial):
    if len(serial)==0:
        return 0,0
    mdd = 0
    peak = serial[0]
    peak_index=0
    drop_length=1
    for i,x in enumerate(serial):
        if x > peak:
            peak = x
            peak_index=i
        dd = (peak - x) / peak
        if dd > mdd:
            mdd = dd
            drop_length=i-peak_index

    return mdd,drop_length


def sum_return_to_daily_return(sum_return):
    daily_return=[0]
    for i in range(1,len(sum_return)):
        if sum_return[i-1]==0:
            daily_return.append(0)
        else:
            daily_return.append((sum_return[i]-sum_return[i-1])/sum_return[i-1])
    return daily_return


def load_calendar(index_path):
    """ load calendar from SH000300 daily."""
    return pd.read_csv(
        os.path.join(index_path, 'SH000300.csv'),
        dtype={'date':str}
    ).iloc[:, 0].tolist()


def read_all_stock_close_ratio(stock_dayk_by_stock_dir):
    #self.allstockclose=dict()
    all_stock_close=dict()
    all_stock_ratio=dict()
    file_list=os.listdir(stock_dayk_by_stock_dir)
    for stock_file in file_list:
        day_close=dict()
        day_ratio=dict()
        stock_file=stock_file[:-4]
        csv_reader=csv.DictReader(open(stock_dayk_by_stock_dir+"/"+stock_file +".csv", encoding='utf-8'))
        for iter, row in enumerate(csv_reader):
            day_close[row['date']]=float(row['close'])/float(row['rate'])
            day_ratio[row['date']]=float(row['rate'])
        all_stock_close[stock_file]=day_close
        all_stock_ratio[stock_file]=day_ratio
    return all_stock_close,all_stock_ratio

'''def read_all_stock_close_ratio_(Stock_MinK_by_Day):
    #self.allstockclose=dict()
    all_stock_close=dict()
    all_stock_ratio=dict()
    file_list=os.listdir(Stock_MinK_by_Day)
    for date in file_list:
        day_close=dict()
        day_ratio=dict()
        stock_file_list=os.listdir(date)
        for stock in stock_file_list:
            stock_file=stock[:-4]
            csv_reader=csv.DictReader(open(Stock_MinK_by_Day+"/"+date+"/"+stock_file +".csv", encoding='utf-8'))
            for iter, row in enumerate(csv_reader):
                day_close[row['date']]=float(row['close'])/float(row['rate'])
                day_ratio[row['date']]=float(row['rate'])
            all_stock_close[stock_file]=day_close
            all_stock_ratio[stock_file]=day_ratio
    return all_stock_close,all_stock_ratio'''

def read_tick(tickfile, close_price=-1):
    csv_reader = csv.DictReader(open(tickfile, encoding='utf-8'))
    tick_list = []
    time_list = []
    close_price = round(close_price, 2)
    for iter, row in enumerate(csv_reader):
        time_list.append(row['time'])
        time = (row['time'])
        if close_price == -1:
            tick = Tick.Tick(str(time), row['price'], row['vol'], -1, -1)  # #第一天开盘，既不涨停又不跌停 或者是美股
        else:
            nowprice = float(row['price'])
            if float(nowprice - close_price >= close_price * 0.098):
                tick = Tick.Tick(str(time), row['price'], row['vol'], 1, -1)  # 涨停
            elif nowprice - close_price <= -close_price * 0.098:
                tick = Tick.Tick(str(time), row['price'], row['vol'], -1, 1)  # 跌停
            else:
                tick = Tick.Tick(str(time), row['price'], row['vol'], -1, -1)

        tick_list.append(tick)  # 将tick加入列表
    return tick_list, time_list

def filter_predict(file_prediction,file_standard):
    
    csv_reader_standerd = csv.DictReader(open(file_standard, encoding='utf-8'))

    reader_prediction = csv.DictReader(open(file_prediction, encoding='utf-8'))
    fieldnames = ['date','code','labels','pct_change','scores']
    csv_writer=csv.DictWriter(open(file_prediction+"_filter", "w"),fieldnames=fieldnames)
    code_list=[]
    for iter, row in enumerate(csv_reader_standerd):
        code_list.append(row['code'])
    csv_writer.writeheader()

    for iter, row in enumerate(reader_prediction):
        if  row['code'] in code_list:
            csv_writer.writerow({'date':row['date'],'code':row['code'],'labels':row['labels'],'pct_change':row['pct_change'],'scores':row['scores']})

def read_min(min_file, close_price=-1):
    #start = time.clock()
    min_list = []
    time_list = []
    if not os.path.exists(min_file) :
       return min_list,time_list

    csv_reader = csv.DictReader(open(min_file, encoding='utf-8'))
    close_price = round(close_price, 2)
    for iter, row in enumerate(csv_reader):
        #timelist.append(row['time'])
        curren_time = row['time']
        min_secods=curren_time.split(':')
        current_min=min_secods[0]
        current_seconds=min_secods[1]
        new_min=current_min.zfill(2)
        new_secods=current_seconds.zfill(2)
        current_time=new_min+new_secods+"00"
        time_list.append(current_time)
        if  float(row['vol'])==0 or float(row['close'])==0:
            current_min = Minute.Minute(str(current_time), 0, 0, -1, -1)
        else:
            now_price = float(row['close'])
            #if "SZ002481" in min_file:
                #print (str(now_price)+" "+str(close_price)+" "+str(min_file)+str( now_price - close_price -( -close_price * 0.080)))
            if close_price == -1:
                current_min = Minute.Minute(str(current_time), now_price, row['vol'], -1, -1)  # #第一天开盘，既不涨停又不跌停 或者是美股
            else:
                if now_price - close_price >= close_price * 0.095:
                    current_min = Minute.Minute(str(current_time), now_price, row['vol'], 1, -1)  # 涨停
                elif now_price - close_price <= -close_price * 0.095:
                    current_min = Minute.Minute(str(current_time), now_price, row['vol'], -1, 1)  # 跌停
                else:
                    current_min = Minute.Minute(str(current_time), now_price, row['vol'], -1, -1)

        min_list.append(current_min)  # 将tick加入列表
    #print("reading minutes data: " + str(time.clock() - start) + " seconds process time")
    return min_list, time_list

def read_min_all(min_file, date, close_price=-1):
    #start = time.clock()
    min_list = []
    time_list = []
    if not os.path.exists(min_file) :
       return min_list,time_list

    csv_reader = csv.DictReader(open(min_file, encoding='utf-8'))
    close_price = round(close_price, 2)
    for iter, row in enumerate(csv_reader):
        if row['date']!= date:
            continue
        #timelist.append(row['time'])
        curren_time = row['time']
        min_secods=curren_time.split(':')
        current_min=min_secods[0]
        current_seconds=min_secods[1]
        new_min=current_min.zfill(2)
        new_secods=current_seconds.zfill(2)
        current_time=new_min+new_secods+"00"
        time_list.append(current_time)
        if  float(row['vol'])==0 or float(row['close'])==0:
            current_min = Minute.Minute(str(current_time), 0, 0, -1, -1)
        else:
            now_price = float(row['close'])
            #print (str(now_price)+" "+str(close_price)+" "+str(min_file))
            if close_price == -1:
                current_min = Minute.Minute(str(current_time), now_price, row['vol'], -1, -1)  # #第一天开盘，既不涨停又不跌停 或者是美股
            else:
                if now_price - close_price >= close_price * 0.098:
                    current_min = Minute.Minute(str(current_time), now_price, row['vol'], 1, -1)  # 涨停
                elif now_price - close_price <= -close_price * 0.098:
                    current_min = Minute.Minute(str(current_time), now_price, row['vol'], -1, 1)  # 跌停
                else:
                    current_min = Minute.Minute(str(current_time), now_price, row['vol'], -1, -1)

        min_list.append(current_min)  # 将tick加入列表
    #print("reading minutes data: " + str(time.clock() - start) + " seconds process time")
    return min_list, time_list

def next_trade_date(calendar, date):
    """ calculate next trade date """
    if date not in calendar:
        raise RuntimeError('date {} is not a valid trade date'.format(date))
    index = calendar.index(date)
    if index == len(calendar) - 1:
        raise RuntimeError('date {} exceed calendar limit'.format(date))
    return calendar[index+1]


def get_next_trading_date(current_date,calendar):
    current_date =  datetime.datetime.strptime(current_date,'%Y%m%d')
    weekday = current_date.weekday()
    sunday_delta = datetime.timedelta(7 - weekday)
    next_monday = (current_date + sunday_delta).strftime('%Y%m%d') 
    # + datetime.timedelta(days=week_period)
    for date in calendar:
          if int(next_monday)<=int(date):
              return date
    print(current_date.strftime('%Y%m%d') +" is not in the history dataset")
    raise RuntimeError('over calendar')
    return None

def get_next_trading_date_week_last_day(current_date,calendar):
    current_date =  datetime.datetime.strptime(current_date,'%Y%m%d')
    weekday = current_date.weekday()
    sunday_delta = datetime.timedelta(6 - weekday)
    next_sunday = (current_date + sunday_delta).strftime('%Y%m%d')  #周末
    # + datetime.timedelta(days=week_period)
    for iter in range(len(calendar)-1):
          if int(calendar[iter]) <= int(next_sunday) and int(calendar[iter+1])>int(next_sunday):
              return calendar[iter]
    print(current_date.strftime('%Y%m%d') +" is not in the history dataset")
    raise RuntimeError('over calendar')
    return None

def parse_prediction(date, code, scores, topk=10, open_time='093500', close_time='143000', stock_period='1D', target_value_percent=0.5,config=None):
    """ parse model prediction into orders.
    currently only support market order.
    
    Parameters
    ----------
    date          : trade date
    code          : trade code
    scores        : user predicted scores with (proba...)
    topk          : number of orders per day

    Returns
    ----------
    orders : orders as list

    Examples
    ----------
    """
    from io import StringIO

    if not config:
        from . import config

    calendar = load_calendar(config.INDEX_PATH)
    calendar_set = set(calendar)
    if stock_period[-1]=='D':
        try:
            day_period=int(stock_period[:-1])
        except Exception as err:  
            print("error when parsing orders")
        next_trade_date_mapping = dict(zip(calendar[:-1], calendar[day_period:]))
    
        

    pred = pd.DataFrame()
    pred['date'] = np.array(date)
    pred['code'] = np.array(code)
    pred['scores'] = np.array(scores)
    pred = pred.groupby('date').apply(
        lambda x: x.sort_values('scores', ascending=False).iloc[:topk]
    ).reset_index(drop=True)


    percent = pred.groupby('date').apply(
        lambda x: target_value_percent / len(x)
    )

    pred['date'] = pred.date.map(lambda x: str(x)[:8])
    pred = pred[pred.date.map(lambda x: x in calendar_set)]
    
    buy = pred
    buy.index = pred.date
    del buy['scores']

    buy['time'] = open_time
    buy['type'] = 'M'
    buy['side'] = 'b'
    buy['percent'] = percent
    
    buy = buy.reset_index(drop=True)

    sell = pd.DataFrame()
    #print(stock_period[-1])
    sell['code'] = buy['code'].values
    if stock_period[-1]=='D':
        try:
            sell['date'] = buy['date'].map(next_trade_date_mapping).values
        except Exception as err:  
            print("error when parsing orders")
    elif stock_period[-1]=='W':
        
        try:
            sell['date'] = buy['date'].apply(lambda x:  get_next_trading_date_week_last_day(x,calendar))
        except Exception as err:  
            print("error when parsing orders")
      
    sell['time'] = close_time
    sell['type'] = 'M'
    sell['side'] = 's'
    sell['percent'] = 0
    
    df = pd.concat([buy, sell])
    #if stock_period[-1]=='D':
    df = df.groupby('date').apply(
    lambda x: x[~x.duplicated(subset=['code'], keep=False)]
    ).reset_index(drop=True)
    #elif 
    #df=df.drop_duplicates()
    
    df = df.sort_values(['date', 'time', 'code'])
    df['param1'] = 0
    df['param2'] = 0
    orders = StringIO(df[['code', 'date', 'time', 'type', 'side', 'percent', 'param1', 'param2']].to_csv(index=False, header=None))

    return orders
    

#返回该股票当天的收盘价,如果没有，一直往前找
    #该函数的返回条件有两个一是找到了收盘价二是一直找到了头
    #current=1获得当天收盘价
    #current=0获得上一天收盘价
'''def getcloseprice(self,code,date,current=0):
        indexx=self.alltradedate.index(date)
        if current==0:
            if indexx<=0:
                return -1
            indexx-=1
            date=self.alltradedate[indexx]
        while True:
            filelist = os.listdir(self.tradedaydir)
            if date+".csv" in filelist:
                csv_reader = csv.DictReader(open(self.tradedaydir+"/"+date+".csv" , encoding='utf-8'))
                for iter, row in enumerate(csv_reader):
                    if row['code']==code:
                        return float(row['close'])/float(row['rate'])
                indexx=indexx-1
                date=self.alltradedate[indexx]
            else:
                if indexx<=0:
                    return -1
                else:
                    indexx=indexx-1
                    date=self.alltradedate[indexx]'''

#返回该股票当天的复权价格,如果没有，一直往前找
#该函数的返回条件有两个一是找到了复权价格二是一直找到了头
#current=1获得当天复权价格
#current=0获得上一天复权价格
'''def getratio(self,code,date,current):
        indexx=self.alltradedate.index(date)
        if current==0:
            if indexx<=0:
                return -1
            indexx-=1
            date=self.alltradedate[indexx]
        while True:
            filelist = os.listdir(self.tradedaydir)
            if date+".csv" in filelist:
                csv_reader = csv.DictReader(open(self.tradedaydir+"/"+date+".csv" , encoding='utf-8'))
                for iter, row in enumerate(csv_reader):
                    if row['code']==code:
                        return float(row['rate'])
                indexx=indexx-1
                date=self.alltradedate[indexx]
            else:
                if indexx<=0:
                    return -1
                else:
                    indexx=indexx-1
                    date=self.alltradedate[indexx]'''

'''def getmiae(self,ticklist,tickindex):
        #print (ticklist[tickindex].time)
        min=ticklist[tickindex].time[0:4]
        totalprice=0
        number=0
        for tick in ticklist:
            if tick.time[0:4]==min:
                totalprice+=tick.price
                number+=1
        return float(totalprice)/number'''



'''def write_file(annual_return,sharp,max_drop,max_drop_length,earn,loss,average_return,):
    import codecs
    writefile=codecs.open("result.html",mode='w')
    writefile.write("<body>年化收益率："+str(annual_return)+"<br/>")
    writefile.write("最大回撤："+str(max_drop)+"<br/>")
    writefile.write("最大回撤持续天数："+str(max_drop_length)+"<br/>")
    writefile.write('<a href="traderecords.txt">成交记录</a><br/>')
    writefile.write("sharp："+str(sharp)+"<br/>")
    writefile.write("盈利次数："+str(earn)+"<br/>")
    writefile.write("亏损次数："+str(loss)+"<br/>")
    writefile.write("单次平均收益："+str(average_return)+"<br/>")
    #writefile.write("委托成功率："+str(sessratio)+"<br/>")
    #writefile.write('每笔交易的收益分布图<br/><div> <iframe width="50%" height="33%" src="basic-line.html"></iframe></div>')
    #writefile.write('成交时长分布图<br/><div> <iframe width="50%" height="33%" src="basic-line.html"></iframe></div>')
    writefile.write('收益曲线<br/><div> <iframe width="50%" height="33%" src="basic-line.html"></iframe></div>')
    writefile.close()'''


'''
    def read_stock_ratio_last_day(self, code, date,currentindex=0):
        index = self.all_trade_date.index(date)
        if currentindex==0:
            if index <= 0:
                return -1
            index -= 1
        date = self.all_trade_date[index]
        if code in self.all_stock_ratio.keys():
            newlist=list(self.all_stock_ratio[code].keys())
            newlistratio = list(self.all_stock_ratio[code].values())
            #
            if not date in newlist:
                newlist = sorted(list(self.all_stock_close[code].keys()))
                for i in range(0, len(newlist)-1):
                    if newlist[i]<=date and (newlist[i+1]>=date or i+1>=len(newlist)-1):
                        return self.all_stock_ratio[code][newlist[i]]
            else:
                index = newlist.index(date)
                return newlistratio[index]
        return -1
'''



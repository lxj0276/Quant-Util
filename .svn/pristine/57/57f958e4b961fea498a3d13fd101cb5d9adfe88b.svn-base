# -*- coding: utf-8 -*-
import csv
import os
import math
import sys
import numpy
import time
import pandas as pd

from . import Order
from . import Stock
from . import TradeOutput
from . import Tick
from . import utils
from . import graph
from . import log


class Trade(object):

    def __init__(self, param, config=None):

        self.min_test = param.get('period', 'minute') == 'minute'
        
        self.initial_cash = param.get('account', 1000000)
        self.total_cash   = self.initial_cash #总现金
        self.day_assets  = dict() #每天的资产变化 等于持仓数量*持仓收盘价+剩余现金

        self.poundage_rate = param.get('commission_rate', 0.0002) #手续费税率
        self.stamp_tax_rate = param.get('tax_rate', 0.001)         #印花税税率
        self.low_bound_poundage = param.get('min_commission', 5)   #手续费下界

        self.logger = log.Logger(self, param.get('log_level', 'ERROR'))
        
        self.benchmark = param.get('benchmark', 'SH000300')
        
        self.order_list = dict() #输入订单 每天对应一个订单list
        self.trade_records = dict() #交易订单记录 ‘091023’ 对应一个交易记录list

        self.stock_repository = dict() #记录当前股票股票数量，股票购入平均价格，所花费的手续费和印花税

        self.isUSStock = str(param.get('stock_type', 0))  #是不是美股 美股没有涨跌停

        self.all_stock_close = dict() #记录所有股票每一天的收盘价格
        self.all_stock_ratio=dict() #记录每只股票每一天的ratio（复权）
        
        if not config:
            from . import config

        self.param = param
        self.config = config
        
        self.tick_dir = config.TICK_PATH
        self.min_dir  = config.MIN_PATH
        self.stock_dayk_by_stock_dir=config.STOCK_PATH
        self.uncompleted_sell_time = config.UNCOMPLETED_SELL_TIME

        self.trade_index_dir = config.INDEX_PATH

        self.current_time = '--'
        
        self.notebook_mode = config.NOTEBOOK_MODE

        # DEBUG: 系统缓存用户结果
        self._task_id = str(int(time.time()*1000))
        self._jpy_user = os.environ.get('JPY_USER', 'default')
        self._docker_path = os.path.join(config.DOCKER_PATH, self._jpy_user)

        self._initialize()


    def _initialize(self):
        if not os.path.exists(self.tick_dir):
            self.logger.error('找不到数据路径:' + self.tick_dir)
            raise RuntimeError
        if not os.path.exists(self.stock_dayk_by_stock_dir):
            self.logger.error('找不到数据路径:' + self.stock_dayk_by_stock_dir)
            raise RuntimeError
        if not os.path.exists(self.trade_index_dir):
            self.logger.error('找不到数据路径:' + self.trade_index_dir)
            raise RuntimeError
        if not os.path.exists(os.path.join(self.trade_index_dir, self.benchmark+ '.csv')):
            index_codes = [x.split('.')[0] for x in os.listdir(self.trade_index_dir)]
            self.logger.error('目前只支持设置以下指数为benchmark:\n'+','.join(index_codes))
            raise RuntimeError
        if self.stamp_tax_rate != 0.001:
            self.logger.error('印花税被修改为%s' % self.stamp_tax_rate)

        start = time.clock()
        self.all_trade_date = utils.load_calendar(self.trade_index_dir)
        self.logger.debug("reading date: "+str(round(time.clock() - start, 6))+" seconds process time")
        start = time.clock()
        self.all_stock_close, self.all_stock_ratio=utils.read_all_stock_close_ratio(self.stock_dayk_by_stock_dir)
        self.logger.debug("reading close and ratio: "+str(round(time.clock() - start, 6))+" seconds process time")

    def _slice_all_trade_date(self, begin_date, end_date):
        self.all_trade_date = [x for x in self.all_trade_date if begin_date<=x<=end_date]
        
    def _set_current_time(self, date, time=''):
        self.current_time = date[:4] + '-' + date[4:6] + '-' + date[6:8]
        if time:
            self.current_time += ' ' + time[:2] + ':' + time[2:4] + ':' + time[4:6]
        
    '''def read_stock_close(self,code,date):
        if code in self.allstockclose.keys():
            if date in self.allstockclose[code].keys():
                closeprice = self.allstockclose[code][date]
                return closeprice
        return -1'''

    # current=0 返回上一天的收盘价格
    # current=1 返回当天的收盘价格
    # 结束条件：找到了收盘价格或者搜索空间遍历完毕
    def read_stock_close(self, code, date, current_index=0):
        index = self.all_trade_date.index(date)
        if current_index==0:
            if index <= 0:
                return -1
            index -= 1
        date = self.all_trade_date[index]
        if code in self.all_stock_close.keys():
            new_list=list(self.all_stock_close[code].keys())
            new_list_close = list(self.all_stock_close[code].values())
            if not date in new_list:
                new_list = sorted(list(self.all_stock_close[code].keys()))
                for i in range(0, len(new_list)-1):
                    if new_list[i]<=date and (new_list[i+1]>=date or i+1>=len(new_list)-1):
                        #print (code+" "+date+" "+new_list[i]+" "+str(self.all_stock_close[code][new_list[i]]))
                        return self.all_stock_close[code][new_list[i]]
                return -1
            else:
                #if code=='SZ002281':
                    #print (new_list)
                    #print (new_list_close)
                    #print(str(index) + " " + code + " " + date + " " + str(self.all_stock_close[code][date]))
                #$index = new_list.index(date)
                #print(str(index) + " " + code + " " + date + " " + str(new_list_close[index]))
                return self.all_stock_close[code][date]#new_list_close[index]
        return -1

    # current=0 返回上一天的复权因子
    # current=1 返回当天的复权因子
    # 结束条件：找到了收盘价格或者搜索空间遍历完毕
    def read_stock_ratio(self, code, date):
        if code in self.all_stock_ratio.keys():
            if date in self.all_stock_ratio[code].keys():
                ratio = self.all_stock_ratio[code][date]
                return ratio
        return -1


    # 处理所有订单
    def trade(self):
        start = time.clock()
        while len(self.order_list)>0:
            day=sorted(self.order_list.items())[0][0] #按天处理
            self._set_current_time(day)
            if self.all_trade_date.index(day)>=len(self.all_trade_date)-1:
                break
            if self.trade_day_orders(day)==-1:
                self.logger.error("交易失败")
                return -1
            self.order_list.pop(day)
            self.logger.debug("trading all orders: " + str(round(time.clock() - start, 6)) + " seconds process time")
            start = time.clock()
        return 1

    def get_neiber_date(self,date):
        for i in range(0, len(self.all_trade_date)-1):
            if int(self.all_trade_date[i])<int(date) and int(self.all_trade_date[i+1])>int(date):
                return i+1,self.all_trade_date[i + 1]
        return -1,-1


    #检查今天需要交易的订单，目的是为了过滤非正常交易日期和停牌股票
    #首先检查date是否为交易日
    #如果不是交易日，将股票找到下一个最近的交易日进行交易
    #如果是交易日，如果该订单交易股票当天停牌，也找到下一个交易日进行交易
    #一切正常的话，扔到今天处理的订单
    def check_order(self,date):
        self._set_current_time(date)
        new_list=[]
        index = self.all_trade_date.index(date)
        if index == -1:
            self.logger.warn(date+"为非交易日期")
        for order in self.order_list[date]:
            if index == -1:
                if order.buy_sell=='s':
                    new_index,new_date=self.get_neiber_date(date)
                    if new_date=='-1':
                        self.logger.warn("订单" + order.code + "于" + date + "交易失败")
                        return -1
                    self.logger.warn("将卖单" + order.code + "挪到" +new_date + "交易")
                    order.date=new_date
                    self.add_order(new_index,order,self.uncompleted_sell_time)
                continue
            today_ratio = self.read_stock_ratio(order.code, date)
            if today_ratio==-1:
                self.logger.warn("没有找到股票" + order.code + "的信息")
                if order.buy_sell=='s':
                    if index >=len(self.all_trade_date)-1:
                        self.logger.warn("该订单" + order.code + "于" + date + "交易失败")
                        return 1
                    new_date = self.all_trade_date[index + 1]
                    self.logger.warn("将卖单" + str(order.code) + "挪到" + str(new_date) + "交易")
                    order.date = new_date
                    self.add_order(index + 1, order, self.uncompleted_sell_time)
            else:
                new_list.append(order)
        self.order_list[date]=new_list
        return 1



    #交易某天的所有订单
    #0. 检查该天交易订单是否有停牌等等
    #1.首先开盘前根据复权修改持仓
    #2.交易订单
    #3.计算当天资产
    def trade_day_orders(self,date):

        # 交易前准备  检查是否有停牌，如果有停牌的卖单，换到下一天
        flag=self.check_order(date)
        if flag == -1:
            return -1

        flag=self.trade_befor_open(date)
        if flag==-1:
            return -1
        #将该天的所有order排序
        daylist=self.sort_order(date)
        #按顺序处理订单
        for order in daylist:
            if not self.min_test:
                flag=self.trade_single_order_tick(order)
            else:
                flag=self.trade_single_order_min(order)
            if flag==-1:
                return -1
        #计算当天总资产
        flag=self.trade_after_close(date)
        if flag==-1:
            return -1
        return 1
    
    #根据复权动态修改持仓
    #读取所有待交易订单，修改数量
    def trade_befor_open(self, date):
        self._set_current_time(date)
        for stock in self.stock_repository.keys():
            todayratio = self.read_stock_ratio(stock, date)
            if todayratio == -1:
                self.logger.warn("没有找到股票" + stock + "的复权价格")
                continue
            self.stock_repository[stock].amounts = math.floor(self.stock_repository[stock].amounts * (
            float(todayratio) / float(self.stock_repository[stock].last_ratio)))
            self.stock_repository[stock].last_ratio = float(todayratio)
        return 1
    
    #计算当天资产
    # 资产等于剩余现金+持仓股票价值
    def trade_after_close(self,date):
        self._set_current_time(date)
        assets=self.total_cash
        for stock in self.stock_repository.keys():
            close=self.read_stock_close(stock,date,1)
            if close ==-1:
                self.logger.error("没有找到股票"+stock+"的收盘价")
                return -1
            else:
                #self.logger.debug(str(self.stock_repository[stock].amounts)+" "+str(close)+" "+str(stock))
                assets+= float(self.stock_repository[stock].amounts) *100* close
                self.stock_repository[stock].close_assets=float(self.stock_repository[stock].amounts) *100* close
        if date in self.day_assets:
            self.logger.error("当日重复交易")
            return -1
        else:
            self.day_assets[date]=assets
            self.logger.info("当前资产" + str(round(assets,2)))
        return 1

    def get_online_close(self, date,time):
        self._set_current_time(date, time)
        assets = self.total_cash
        currentindex = self.all_trade_date.index(date)

        for stock in self.stock_repository.keys():

            minfile = self.min_dir + "/" + date + "/" + stock + ".csv"

            minlist, timelist = utils.read_min(minfile, -1)
            if len(minlist) == 0 and len(timelist) == 0:
                assets+=self.stock_repository[stock].close_assets

            if time not in timelist:
                if  self.stock_repository[stock].close_assets==-1:
                    self.logger.error("没有找到股票"+stock+" 在  "+time+"的实时价格")
                    return -1
                assets += self.stock_repository[stock].close_assets
            else:
                min_index=timelist.index(time)
                assets+=  self.stock_repository[stock].amounts*100*minlist[min_index].price
            self.online_assets = assets
        return assets


        # 交易当天所有股票
        # 如果是买单，当天没买完就算了，如果是卖单，当天没卖完就接着卖
        # 1.美股去掉涨跌停
        # 2.检查股票数据是否有误
        # 3.读取股票当天交易的所有数据
        # 4.交易
    def trade_single_order_min(self, order):
        '''if order.date not in self.alltradedate:
            print('[WARN ' + order.date + '] ' + '订单股票' + order.code + '查无记录')
            return -1'''
        self._set_current_time(order.date, order.time)
        currentindex = self.all_trade_date.index(order.date)
        minfile = self.min_dir + "/" + order.date + "/" + order.code + ".csv"
        if self.isUSStock == '0':  # 不是美股
            closeprice = self.read_stock_close(order.code, order.date, 0)
        else:
            closeprice = -1  # -1意味着没有涨跌停

        flag = self.check_order_error(order, minfile,ismin=1)
        if flag == -1:
            return -1
        if flag == -2:
            return 0

        minlist, timelist = utils.read_min(minfile, closeprice)
        if len(minlist)==0 and len(timelist)==0:
            self.logger.warn('没有找到股票' + order.code + '的数据，卖单推迟到下一交易日')
            if currentindex < len(self.all_trade_date) - 1:
                currentindex += 1
                order.date = self.all_trade_date[currentindex]
                self.add_order(currentindex, order, self.uncompleted_sell_time)
                return -2

        # 获取当前位置
        minindex = utils.get_index(timelist, order.time)
        #检查当前位置是否超过了最大交易时间
        flag = self.check_warning(minindex, timelist, order, currentindex) #flag=1 代表当前位置超过了最大交易时间
        #print(str(flag) + " " + order.code+" "+order.buy_sell+" "+str(minindex)+" "+str(minlist[minindex].count))
        if flag == 1:
            return 1
        else:
            if order.buy_sell=='b':
                flag = self.buy_min(order, minlist, minindex)
            else:
                flag=self.sell_min(order, minlist, minindex)
            if flag == -1:
                return -1

    #交易当天所有股票
    #如果是买单，当天没买完就算了，如果是卖单，当天没卖完就接着卖
    #1.美股去掉涨跌停
    #2.检查股票数据是否有误
    #3.读取股票当天交易的所有数据
    #4.交易
    def trade_single_order_tick(self,order):
        self._set_current_time(order.date, order.time)
        if order.date not in self.all_trade_date:
            self.logger.warn('订单股票' + order.code + '查无记录')
            return -1
        currentindex=self.all_trade_date.index(order.date)
        tickfile = self.tick_dir + "/" + self.all_trade_date[currentindex] + "/" + order.code + ".csv"
        if self.isUSStock=='0':  #不是美股
            closeprice=self.read_stock_close(order.code,order.date,0)
        else:
            closeprice=-1  #-1意味着没有涨跌停
        flag=self.check_order_error(order,tickfile)
        if flag==-1:
            return -1
        if flag==-2:
            return 0
        ticklist, timelist=utils.read_tick(tickfile,closeprice) #读所有的tick文件
        #获取当前tick
        tickindex=utils.get_index(timelist,order.time)

        #检查超过了最大交易时间
        flag=self.check_warning(tickindex,timelist,order,currentindex)
        if flag==1:
            return 1
        else:
            if order.buy_sell=='b':
                flag=self.buy_tick(order,ticklist,tickindex)
            else:
                flag = self.sell_tick(order, ticklist, tickindex)
            if flag==-1:
                return -1
            else:
                return 1


    # 买单根据剩余的钱决定购买数量
    # 1.检查是否超过最大处理量， 如果超过最大处理量（超过当天最大交易时间） 交易结束
    # 2.计算交易手数量
    # 3.如果交易数量小于等于零手，说明交易结束，增加交易记录
    # 4.开始交易
    # 5.交易失败，返回
    # 6.交易成功增加交易记录
    # 7.如果没有全部买完，打印提示warning信息
    def buy_min(self,order,minlist,minindex):
        self._set_current_time(order.date, order.time)
        online_assets=self.get_online_close(order.date,order.time)
        if online_assets==-1:
            return -1
        currentcapital = online_assets * (float)(order.buy_portion)  #如果是买单，代表待交易股票总额
        #currentcapital=self.total_cash*(float)(order.buyPortion )#如果是买单，代表待交易股票总额
        if currentcapital >= self.total_cash:
            currentcapital = self.total_cash
        # 计算可交易数量
        currentprice = minlist[minindex].price  # 当天交易价格
        count = (int)(float(minlist[minindex].count) *0.25) # 当前可交易数据
        #print (str(count)+"当前分钟交易数量 " +order.code)
        if count <=0:
            self.logger.warn('订单股票' + order.code + '交易不足')
            return
        currentamounts = self.get_max_buy_amounts(0, currentcapital, currentprice)  # 检查当前资金可以购买多少手的股票
        # 检查是否可以购买1手
        if currentamounts <=0:
            self.logger.warn("当前价格" + order.code + "无法下单")
            return
        # 交易股票
        if count >= currentamounts:
            stockCost_, amountCount_ = self.make_trade(order, minlist[minindex], currentamounts, currentprice)
        else:
            stockCost_, amountCount_ = self.make_trade(order, minlist[minindex], (int)(count), currentprice)
        # 交易失败
        if stockCost_ == -1 and amountCount_ == -1:  # 表示当前分钟无法交易 卖单推到后一天
            self.logger.warn('订单股票' + order.code + '因数量不够交易不足')
            return
        else:

            self.add_trade_recoders(order, stockCost_, amountCount_, minlist[minindex].time)
        if not count >= currentamounts:  # 如果不能在此分钟全部交易
            self.logger.warn('订单股票' + order.code + '交易不足')
        return


    #1.检查是否超过最大处理量， 如果超过最大处理量（超过当天最大交易时间） 交易结束
    #2.计算交易手数量
    #3.如果交易数量小于等于零手，继续下一个分钟交易
    #4.开始交易
    #5.如果交易失败，调到下一个分钟交易
    #6.修改变量
    #7.如果不能在此分钟交易完全，继续下一个分钟交易
    #8.否则增加交易记录
    def sell_min(self,order,minlist,minindex):
        self._set_current_time(order.date, order.time)
        stockcost = 0.0  # 交易股票价值
        amountcount = 0.0  # 已经交易股票数
        order.amounts = self.stock_repository[order.code].amounts # 如果是卖单，需要读取当前仓库剩余数量
        currentamounts=order.amounts #如果是卖单，代表待交易股票数量
        initialmin = minindex
        while True:
            if minindex >= len(minlist)-1 or minindex >= initialmin+1 or (order.type == 'L' and float(minindex) - float(initialmin) > order.valid_duration):
                self.record_overtime_orders(order, stockcost, amountcount, minlist[minindex-1].time,currentamounts)
                return
            #计算可交易数量
            currentprice= minlist[minindex].price #当天tick交易价格
            count = (int)(((float(minlist[minindex].count)) ) *0.25)#当前tick可交易数据
            if currentamounts <= 0:
                self.logger.warn("当前价格" + order.code + "无法下单")
                minindex += 1
                continue
            if count<=0:
                #self.add_trade_recoders(order, stockcost, amountcount, minlist[minindex - 1].time)
                #print('[WARN ' + order.date + '] ' + '订单股票' + order.code + '交易不足')
                minindex+=1
                continue
            #交易股票
            if count >= currentamounts :
                stockCost_, amountCount_=self.make_trade(order,minlist[minindex],currentamounts,currentprice)
            else:
                stockCost_, amountCount_ = self.make_trade(order, minlist[minindex],(int)(count),currentprice)
            #交易失败
            if stockCost_ == -1 and amountCount_ == -1: #表示当前分钟无法交易 卖单推到后一天

                minindex += 1
                continue

            amountcount += amountCount_
            stockcost += stockCost_
            currentamounts -= amountCount_

            #交易成功
            if  currentamounts>0:  # 如果不能在此分钟全部交易
                minindex += 1
                continue
            else:
                self.add_trade_recoders(order, stockcost, amountcount, minlist[minindex].time)
            return

    # 买单根据剩余的钱决定购买数量
    # 1.检查是否超过最大处理量， 如果超过最大处理量（超过当天最大交易时间，或者交易时间超过了20个tick） 交易结束
    # 2.计算交易手数量
    # 3.如果交易数量小于等于零手，说明交易结束，增加交易记录
    # 4.开始交易
    # 5.如果交易失败，调到下一个tick
    # 6.如果交易成功，修改变量
    def buy_tick(self, order, ticklist, tickindex):
        self._set_current_time(order.date, order.time)
        stockcost = 0.0  # 交易股票价值
        amountcount = 0.0  # 已经交易股票数
        #online_assets = self.get_online_close(order.date, order.time) + self.total_cash
        currentcapital =self.total_cash*(float)(order.buy_portion)  # 如果是买单，代表待交易股票总额
        # currentcapital=self.total_cash*(float)(order.buyPortion )#如果是买单，代表待交易股票总额
        if currentcapital >= self.total_cash:
            currentcapital = self.total_cash
        initialTick = tickindex
        while True:
            # 如果已经超过当前最大处理数量 交易结束，增加超时订单处理
            if tickindex >= len(ticklist) or (tickindex >= initialTick + 1) or (order.type == 'L' and float(tickindex) - float(initialTick) > order.valid_duration): #or (tickindex >= initialTick + 20)
                self.record_overtime_orders(order, stockcost, amountcount, ticklist[tickindex - 1].time)
                return
            # 计算交易手数量
            currentprice = ticklist[tickindex].price  # 当天tick交易价格
            count = (int)((float(ticklist[tickindex].count)))  # 当前tick可交易数据
            if count == 0:
                tickindex += 1
                continue
            currentamounts = self.get_max_buy_amounts(stockcost, currentcapital,currentprice)  # 检查当前资金可以购买多少手的股票
            # 检查是否可以购买1手
            if currentamounts <=0:
                if stockcost != 0:
                    self.add_trade_recoders(order, stockcost, amountcount, ticklist[tickindex - 1].time)
                else:
                    self.logger.warn("当前价格" + order.code + "无法下单")
                return
            # 交易股票
            if count >= currentamounts:
                stockCost_, amountCount_ = self.make_trade(order, ticklist[tickindex], currentamounts,currentprice)
            else:
                stockCost_, amountCount_ = self.make_trade(order, ticklist[tickindex], (int)(count),currentprice)
            # 交易失败
            if stockCost_ == -1 and amountCount_ == -1:  # 表示当前tick无法交易
                tickindex += 1
                continue
            # 修改变量
            stockcost += stockCost_
            amountcount += amountCount_
            currentamounts-=amountCount_
            pundagecost, stampTaxCost = self.compute_poundage_cost(stockcost)
            if (currentamounts<=0):  # 如果可在此tick全部交易
                self.add_trade_recoders(order, stockcost, amountcount, ticklist[tickindex - 1].time)
                return
            else:
                tickindex += 1
            currentcapital -= (stockCost_ - pundagecost)  # 当前订单账户余额

    # 买单根据剩余的钱决定购买数量
    # 1.检查是否超过最大处理量， 如果超过最大处理量（超过当天最大交易时间，或者交易时间超过了20个tick） 交易结束
    # 2.计算交易手数量
    # 3.如果交易数量小于等于零手，说明交易结束，增加交易记录
    # 4.开始交易
    # 5.如果交易失败，调到下一个tick
    # 6.如果交易成功，修改变量
    def sell_tick(self, order, ticklist, tickindex):
        stockcost = 0.0  # 交易股票价值
        amountcount = 0.0  # 已经交易股票数
        order.amounts = self.stock_repository[order.code].amounts  # 如果是卖单，需要读取当前仓库剩余数量
        currentamounts = int(order.amounts)  # 如果是卖单，代表待交易股票数量
        initialTick = tickindex
        while True:
            # 如果已经超过当前最大处理数量 交易结束，增加超时订单处理
            if tickindex >= len(ticklist) or (tickindex >= initialTick + 20) or (order.type == 'L' and float(tickindex) - float(initialTick) > order.valid_duration):
                self.record_overtime_orders(order, stockcost, amountcount, ticklist[tickindex - 1].time,currentamounts)
                return
            # 计算交易数量
            currentprice = ticklist[tickindex].price  # 当天tick交易价格
            count = (int)((float(ticklist[tickindex].count)))  # 当前tick可交易数据
            if count <=0:
                tickindex += 1
                continue
            ''''# 检查是否可以购买1手
            if currentamounts<= 0:
                if stockcost != 0:
                    self.add_trade_recoders(order, stockcost, amountcount, ticklist[tickindex - 1].time)
                else:
                    print("[WARN " + order.date + "] " + "当前价格" + order.code + "无法下单")
                return'''
            # 交易股票
            if count >= currentamounts:
                stockcost_, amountcount_ = self.make_trade(order, ticklist[tickindex], currentamounts,
                                                                currentprice)
            else:
                stockcost_, amountcount_ = self.make_trade(order, ticklist[tickindex], (int)(count),currentprice)
            # 交易失败
            if stockcost_ == -1 and amountcount_ == -1:  # 表示当前tick无法交易
                tickindex += 1
                continue
            # 修改变量
            stockcost += stockcost_
            amountcount += amountcount_
            currentamounts-=amountcount_
            if (currentamounts<=0):  # 如果可在此tick全部交易
                self.add_trade_recoders(order, stockcost, amountcount, ticklist[tickindex - 1].time)
                return
            else:
                tickindex += 1
                currentamounts -= amountcount_


    # 输入订单，tick,数量，价格
    # 返回当前tick交易股票总价，手续费，印花税（购入为零）
    # 如果涨停则不能买入
    # 如果跌停则不能卖出
    def market_trade(self, order, tick, currentAmounts, currentPrice):
        self._set_current_time(order.date, order.time)
        if order.code in self.stock_repository.keys():  # 如果股票池中有该股票的话
            if order.buy_sell == 'b' and tick.up_stop_point == -1:
                self.stock_repository[order.code].update(currentAmounts, currentPrice)
            elif order.buy_sell == 's' and tick.down_stop_point == -1:
                self.stock_repository[order.code].amounts -= currentAmounts  # 减少
            else:
                return -1, -1
        else:  # 股票池中没有该股票 只有增加 没有减少 因为之前判断过
            #print (order.code+" "+str(tick.up_stop_point)+" "+tick.time+" "+str(tick.price))
            if order.buy_sell == 'b' and tick.up_stop_point == -1:
                stock = Stock.Stock(order.code, currentAmounts, currentPrice, order.date)
                stock.last_ratio = self.read_stock_ratio(stock.code, order.date)
                if stock.last_ratio == -1:
                    self.logger.warn("没有找到股票" + order.code + "的复权价格")
                    return -1, -1
                self.stock_repository[order.code] = stock  # 增加
            else:
                return -1, -1
        stockCost = currentAmounts * currentPrice*100 # 买入或者卖出股票价值
        amountCount = currentAmounts  # 买入或者卖出股票数量
        return stockCost, amountCount

    # 返回当前tick交易股票总价，手续费，印花税（购入为零）
    def limit_trade(self, order, tick, currentAmounts, currentPrice):
        self._set_current_time(order.date, order.time)
        if order.code in self.stock_repository.keys():  # 如果股票池中有该股票的话
            if order.buy_sell == 'b' and order.l_price >= currentPrice and tick.up_stop_point != 1:
                self.stock_repository[order.code].update(currentAmounts, currentPrice)
            elif order.buy_sell == 's' and order.l_price <= currentPrice and tick.down_stop_point != 1:
                self.stock_repository[order.code].amounts -= currentAmounts  # 减少
            else:
                return -1, -1,
        else:  # 股票池中没有该股票 只有增加 没有减少
            if order.buy_sell == 'b' and order.l_rice >= currentPrice and tick.up_stop_point != 1:
                stock = Stock.Stock(order.code, currentAmounts, currentPrice, order.date)
                stock.last_ratio = self.read_stock_ratio(stock, order.date)
                if stock.last_ratio == -1:
                    self.logger.warn("没有找到股票" + order.code + "的复权价格")
                    return -1, -1
                self.stock_repository[order.code] = stock  # 增加
            else:
                return -1, -1
        stockCost = currentAmounts * currentPrice*100  # 买入或者卖出股票价值
        amountCount = currentAmounts  # 买入或者卖出股票数量
        return stockCost, amountCount  # ,pundageCost,stampCost

    def make_trade(self, order, tick, currentAmounts, currentPrice):
        if order.type == 'L':
            stockCost, amountCount = self.limit_trade(order, tick, currentAmounts, currentPrice)
            return stockCost, amountCount
        elif order.type == 'M':
            stockCost, amountCount = self.market_trade(order, tick, currentAmounts, currentPrice)
            return stockCost, amountCount
        else:
            return -1, -1

    def add_trade_recoders(self,order,stockCost,amountCount,time):
        pundageCost, stampTaxCost = self.compute_poundage_cost(stockCost)
        if order.buy_sell == 's':
            self.total_cash += (stockCost - pundageCost - stampTaxCost)

            sellvalue = stockCost - pundageCost - stampTaxCost

            buyvalue = (self.stock_repository[order.code].average_price) * amountCount*100 # +self.stockRepository[order.code].pundageCost*(float(amountCount/self.stockRepository[order.code].amounts))
            #print (str(sellvalue)+" buyvalue"+str(buyvalue))
            earnorloss = (sellvalue - buyvalue) / buyvalue
            if self.stock_repository[order.code].amounts == 0:
                self.stock_repository.pop(order.code)
        else:
            earnorloss = 0
            self.total_cash-=(stockCost + pundageCost)
            self.stock_repository[order.code].pundage_cost=pundageCost

        # 增加回测记录
        if order.date in self.trade_records:
            self.trade_records[order.date].append(
                TradeOutput.TradeOutput(order, time, (stockCost / amountCount/100), amountCount,earnorloss,pundageCost, stampTaxCost))
        else:
            newlist=[]
            newlist.append(
                TradeOutput.TradeOutput(order, time, (stockCost / amountCount/100), amountCount,earnorloss,pundageCost, stampTaxCost))
            self.trade_records[order.date]=newlist

    def get_index_returns(self, code, days):
        dates = [x.replace('-', '') for x in days]
        fname = os.path.join(self.trade_index_dir, code + '.csv')
        with open(fname, 'r') as f:
            data = [x.strip().split(',') for x in f][1:]
        data = [x[1] for x in data if x[0] in dates]
        data = numpy.array(data, dtype=numpy.float)
        data /= data[0]
        return data
    
    def report(self, return_report=False):
        dayreturns=[] #每日收益
        days=[] #每个交易日
        tradereturn=[] #每笔交易的收益（卖单）
        tradeearn=0 #盈利单子总数
        tradeloss=0#亏损单子总数
        sharp=0 #sharpe ratio
        annualreturn=0 #年化收益率
        newlist=sorted(self.trade_records.items())
        for (i,item) in enumerate(newlist): #traderecods是个字典，存的是每一天的交易订单
            tradeday=item[0]
            days.append(tradeday[0:4]+"-"+tradeday[4:6]+"-"+tradeday[6:8])
            if self.initial_cash>0: #加进每日收益
                dayreturns.append(self.day_assets[tradeday] / self.initial_cash)
            else:
                dayreturns.append(0)
            for k in self.trade_records[tradeday]: #遍历tradeday的每一笔订单，如果是卖单，记录是否盈利，是否亏损
                if k.buy_sell=='s':
                    tradereturn.append(k.stock_return)
                    if k.stock_return>0:
                        tradeearn+=1
                    elif k.stock_return <0:
                        tradeloss+=1
        if len(self.trade_records)>=2: #记录年化收益率
            begin=self.all_trade_date.index(sorted(self.trade_records.items())[0][0]) #第一天
            end=self.all_trade_date.index(sorted(self.trade_records.items())[-1][0]) #最后一天
            annualreturn=math.pow(dayreturns[-1], 250/(end-begin))-1

            dailyreturn=utils.sum_return_to_daily_return(dayreturns)
            dayreturnstd=numpy.std(dailyreturn, ddof=1)
            if dayreturnstd==0:
                sharp=0
            else:
                sharp=(annualreturn-0.04)/(dayreturnstd*numpy.sqrt(250))

            maxdropdown, maxdropdays = utils.max_drop_down(dayreturns)

            indexreturns = self.get_index_returns(self.benchmark, days)  # TODO: 修正没有交易日期的账户资产
            indexannualreturn = math.pow(indexreturns[-1], 250 / (end - begin)) - 1

            table = [
                (u'回测收益', str(round((dayreturns[-1] - 1) * 100, 2)) + '%'),
                (u'年化收益', str(round(annualreturn * 100, 2)) + '%'),
                (u'基准收益', str(round((indexreturns[-1] - 1) * 100, 2)) + '%'),
                (u'基准年化收益', str(round(indexannualreturn * 100, 2)) + '%'),
                (u'夏普比率', str(round(sharp, 3))),
                (u'最大回撤', str(round(maxdropdown * 100, 3)) + '%'),
                (u'最大回撤天数', str(maxdropdays)),
                (u'盈利次数', str(tradeearn)),
                (u'亏损次数', str(tradeloss)),
                (u'单次平均收益', str(round(numpy.mean(tradereturn) * 100, 3)) + '%'),
            ]

            # 记录用户回测结果
            with open(self._docker_path + '/backtest.txt', 'a') as f:
                table_as_string = [': '.join(x) for x in table]
                f.write('task_id: ' + self._task_id + '; ')
                f.write('; '.join(table_as_string) + '\n')

            table = list(map(list, zip(*table)))  # transpose
            dayreturns = numpy.array(dayreturns) - 1
            indexreturns = numpy.array(indexreturns) - 1
            dayreturns = numpy.round(dayreturns * 100, 4)
            indexreturns = numpy.round(indexreturns * 100, 4)
            fig = graph.plot_charts(days, dayreturns, indexreturns, table, notebook_mode=self.notebook_mode)
        else:
            self.logger.error("没有交易记录")

        if not return_report:
            return fig

        # return report
        _report = dict()
        _report['days'] = days
        _report['returns'] = dayreturns
        _report['benchmark'] = indexreturns
        return fig, _report

    
    def submit(self, pred=None, order=None):

        read_order = self.param.get('read_order', False)
        order_path = self.param.get('order_path', "order.csv")

        if read_order:
            orders = pd.read_csv(order_path)
        elif str(order) != 'None':
            from io import StringIO
            
            orders = StringIO(order.to_csv(index=False, header=None))
        else:
            # 解析订单
            topk = self.param.get('order_topk', 10)
            open_time = self.param.get('order_open_time', '093500')
            close_time = self.param.get('order_close_time', '143000')
            date = pd.to_datetime(pred['date'].astype('str')).map(
                lambda x: x.strftime('%Y%m%d'))  # input can be datetime or string or int
            # print (date)
            code = pred.code.map(lambda x: x.split('_')[-1])  # input can be SH600000 or CN_STK_600000
            scores = pred.scores
            stock_period = self.param.get('stock_period', '1D')
            target_value_percent = self.param.get('target_value_percent', 0.5)


            orders = utils.parse_prediction(date, code, scores, topk, open_time, close_time, stock_period,
                                            target_value_percent, self.config)
            '''with open('orders.csv', 'w') as f:
                f.write(orders.read())
                orders.seek(0)'''
            # 记录用户预测提交
            if not os.path.exists(self._docker_path):
                os.makedirs(self._docker_path)
                os.chmod(self._docker_path, 0o777)
            pred.to_csv(self._docker_path + '/prediction_{}.csv'.format(self._task_id), index=False)
            with open(self._docker_path + '/orders_{}.csv'.format(self._task_id), 'w') as f:
                f.write(orders.read())
                orders.seek(0)

        start = time.clock()
        csv_reader = csv.reader(orders)
        # 初始化订单和模型
        totalportion=0
        begin_date = '20991231'
        end_date   = '19000101'
        for row in csv_reader:
            code, date, timeorder, type, buy_sell, buyPortion, limitPrice, validDuration = row
            begin_date = min(date, begin_date)
            end_date   = max(date, end_date)
            if buy_sell!='s' and buy_sell!='b':
                self.logger.error("购买或者卖出字段仅接受b或者s,订单无效")
                return -1
            if type!='L'  and type!='M':
                self.logger.error("订单类型仅接受L或者M字段,订单无效")
                return -1
            if  buy_sell=='b' and(float(buyPortion)<=0 or float(buyPortion)>1):
                self.logger.error("购买比例仅接受0到1之间的值")
                return -1
            if buy_sell=='b':
                totalportion+=float(buyPortion)
            if float(validDuration)<=0 and type=='L':
                self.logger.error("限价单有效时间不应该小于等于零")
                return -1
                
            # 限价单以元为单位 #输入订单要求按天排序
            order = Order.Order(code, date, timeorder, type, buy_sell, buyPortion, limitPrice, validDuration)  # 初始化订单
            index=self.all_trade_date.index(order.date)
            assert  index!=-1
            self.add_order(index,order,order.time)
        self.logger.debug("reading order: "+str(round(time.clock() - start, 6))+" seconds process time")

        # 截断交易日期
        self._slice_all_trade_date(begin_date, end_date)
        
        return 0

    # 记录最大购买数量
    def get_max_buy_amounts(self,stockcost, currentcapital, currentprice):
        currentamounts = math.floor((float)(currentcapital) / (((float)(currentprice)) * 100))  # 还需要处理的股票数量
        while currentamounts >= 0:
            fee, _ = self.compute_poundage_cost(stockcost + currentprice * 100 * currentamounts)
            if fee + currentprice * 100 * currentamounts <= currentcapital:
                return currentamounts
            currentamounts -= 1
        return 0

    # 计算手续费和印花税
    def compute_poundage_cost(self, totalcaptial):
        if (totalcaptial * self.poundage_rate <= self.low_bound_poundage):
            return self.low_bound_poundage, self.stamp_tax_rate * totalcaptial
        else:
            return totalcaptial * self.poundage_rate, totalcaptial * self.stamp_tax_rate

    # 将某一天的订单排序
    # 先按tick时间排序
    # 同一天先处理卖单再处理买单
    def sort_order(self, date):
        # 分成tick 按tick时间分类订单
        tickorder = {}
        for order in self.order_list[date]:
            if order.time in tickorder:
                tickorder[order.time].append(order)
            else:
                newlist = []
                newlist.append(order)
                tickorder[order.time] = newlist
        # 同一tick先处理卖单再处理买单
        for tick in tickorder:
            list = tickorder[tick]
            newlist = []
            for order in list:
                if order.buy_sell == 's':
                    newlist.append(order)
            for order in list:
                if order.buy_sell == 'b':
                    newlist.append(order)
            tickorder[tick] = newlist
        # 按tick顺序排序
        daylist = []
        newlist = sorted(tickorder.items())
        for item in newlist:
            for order in item[1]:
                daylist.append(order)
        return daylist

    
    #记录超时订单
    def record_overtime_orders(self,order,stockcost,amountcount,time,leftamount=0):
        self._set_current_time(order.date, order.time)
        self.logger.warn('订单股票' + order.code + '交易不足')
        if order.buy_sell == 'b' and stockcost != 0:
            self.add_trade_recoders(order, stockcost, amountcount, time)
        if order.buy_sell == 's':
            cindex = self.all_trade_date.index(order.date)
            if amountcount != 0:
                self.add_trade_recoders(order, stockcost, amountcount,  time)
            if cindex < len(self.all_trade_date) - 1:
                self.add_order(cindex + 1, order, self.uncompleted_sell_time)

    def check_order_error(self, order, tickfile,ismin=0):
        self._set_current_time(order.date, order.time)
        if not os.path.exists(tickfile) and order.buy_sell=='b':
            self.logger.warn('没有找到股票' + order.code + '的数据，买单取消')
            return -2
        if ismin==0:
            if not os.path.exists(tickfile):
                self.logger.warn('没有找到股票' + order.code + '的数据，卖单推迟到下一交易日')
                if order.buy_sell=='s':
                    cindex=self.all_trade_date.index(order.date)
                    if cindex<len(self.all_trade_date)-1:
                        cindex+=1
                        order.date=self.all_trade_date[cindex]
                        order.time=self.uncompleted_sell_time
                        self.add_order(cindex,order,order.time)
                        return -2
                else:
                    return -1
        if order.buy_sell == 's' and  order.code in self.stock_repository.keys() and order.date==self.stock_repository[order.code].buy_date:
            self.logger.warn('订单股票'+order.code+'无法在当日卖出')
            cindex=self.all_trade_date.index(order.date)
            return -2
        # 如果该股票是卖出单，判断是否仓库中是否有该股票
        if order.buy_sell == 's' and not order.code in self.stock_repository.keys():
            self.logger.warn('订单股票'+order.code+'没有持仓卖出')
            return -2
        return 0




    def check_warning(self,tickindex,timelist,order,currentindex):
        self._set_current_time(order.date, order.time)
        if tickindex<0:
            self.logger.warn('订单股票' + order.code + '超过规定时间无法购入')
            return 1
        if tickindex>=len(timelist)-1 and order.buy_sell=='b':  ##容错处理
            self.logger.warn('订单股票'+order.code+'超过规定时间无法购入')
            return 1
        elif tickindex>=len(timelist)-1 and order.buy_sell=='s':
            self.logger.warn('订单股票'+order.code+'当天无法卖出')
            currentindex+=1
            self.add_order(currentindex,order,self.uncompleted_sell_time)  #没有卖出去，添加到后一天的订单
            return 1
        else:
            return 0

    '''def getAssets(self, day, time):
        asset = float(self.total_cash)
        print("total cash: " + str(asset))
        print("stock reposity")
        for stock in self.stock_repository:
            index = self.all_trade_date.index(day)
            price = self.get_price(stock, index, time)
            if price == -1:
                print("没有找到该股票的价格" + stock)
                return -1
            else:
                asset += self.stock_repository[stock].amounts * float(price) * 100
            #print("stock: " + stock + " price： " + price + " amounts: " + str(self.stock_repository[stock].amounts))
        return asset'''

    def add_order(self,day,order,time):
        if self.all_trade_date[day] in self.order_list:
            order.time = time
            order.date = self.all_trade_date[day]
            self.order_list[order.date].append(order)
        else:
            newlist = []
            order.time = time
            order.date = self.all_trade_date[day]
            newlist.append(order)
            self.order_list[order.date] = newlist


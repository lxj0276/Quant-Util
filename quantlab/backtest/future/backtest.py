# -*- coding: utf-8 -*-
# author: evanzd <dongzhou@pku.edu.cn>

import os
import re
import numpy as np
import pandas as pd
from . import env
from .log import Logger
from .utils import is_tradetme
from .plots import plot_chart
from .feeds import Feed
from .orders import MarketOrder


class BackTest(object):
    """期货回测"""

    def __init__(self, param):
        self._account         = param.get('account', 100000.0)
        self._margin_rate     = param.get('margin_rate', 0.11)
        self._commission_rate = param.get('commission_rate', '0.0001')
        self._scaler          = param.get('scaler', 10)
        self._risk_degree     = param.get('risk_degree', 0.3)
        self._slippage        = param.get('slippage', True)
        self._notebook_mode   = param.get('notebook_mode', True)
        self._position        = 0.0
        self._position_cost   = 0.0
        self._market_data     = None
        self._account_hist    = []
        self._trade_hist      = []

        log_level = param.get('log_level', 'WARN')
        self.logger = Logger(self, log_level)

    @property
    def available(self):
        if self._market_data is None: return self._account/self._margin_rate*self._risk_degree
        return max(self._account/self._margin_rate*self._risk_degree - abs(self._position)*self._scaler*self._market_data.price, 0)

    @property
    def cash(self):
        if self._market_data is None: return self._account
        return self._account - abs(self._position)*self._scaler*self._market_data.price*self._margin_rate

    @property
    def current_time(self):
        if self._market_data is None: return '--'
        return self._market_data.time
    
    def check_close(self, signal, ticks):
        found = self.read_next_tick(ticks, signal.time)
        need_close = True
        if self.cash < 0:
            self.logger.info('保证金不足，平仓')
        elif self._position > 0 and signal.long == -1:
            self.logger.info('收到平多仓信号，平仓')
        elif self._position < 0 and signal.short == -1:
            self.logger.info('收到平空仓信号，平仓')
        elif self._position > 0 and signal.short == 1:
            self.logger.info('信号由多转空，平仓')
        elif self._position < 0 and signal.long == 1:
            self.logger.info('信号由空转多，平仓')
        else:
            need_close = False
        if not need_close: return
        order = MarketOrder(abs(self._position), self._market_data.time)
        self.logger.info('创建平仓订单成功，平仓数量%d'%order.amount_total)
        while order.amount > 0:
            if not found: # end of tick, force close
                self.logger.warn('未找到数据，以最后一个Tick近似成交')
                if self._slippage:
                    price = self._market_data.ask1*1.0005 if self._position < 0 else self._market_data.bid1*0.9995 #0.05% slippage
                else:
                    price = self._market_data.price*1.0005 if self._position < 0 else self._market_data.price*0.9995 #0.05% slippage
                amount = order.amount
            else:
                if self._slippage:
                    price = self._market_data.ask1 if self._position < 0 else self._market_data.bid1
                else:
                    price = self._market_data.price
                amount = min(order.amount, int(0.1*self._market_data.asize1) if self._position < 0 else int(0.1*self._market_data.bsize1))
            if amount > 0:
                value  = amount*price*self._scaler
                profit = np.sign(self._position)*(value-self._position_cost*amount/abs(self._position))-value*self._commission_rate
                self._position_cost *= 1 - amount/abs(self._position)
                self._position -= np.sign(self._position)*amount
                self._account  += profit
                order.amount_traded += amount
                self.logger.info('平仓数量%d，平仓价格%.2f，平仓收益%.2f，当前总仓位%d，当前总资产%.2f，当前可用资金%.2f'%(
                    amount, price, profit, self._position, self._account, self.available))
                self._trade_hist.append((self._market_data.time, 'close', amount, price, self._position, self._account))
            self.read_next_tick(ticks)

    def check_open(self, signal, ticks):
        if not (signal.long == 1 or signal.short == 1): return
        if not is_tradetme(signal.time): return
        if signal.long == 1 and self._position < 0: return
        if signal.short == 1 and self._position > 0: return
        found = self.read_next_tick(ticks, signal.time)
        if not found:
            self.logger.warn('当前时间未找到有效Tick数据')
            return
        if signal.long == 1: # buy
            amount = self.available // (self._market_data.price * self._scaler * (1 + self._commission_rate))
            if amount == 0: return
            order  = MarketOrder(amount, self._market_data.time)
            self.logger.info('收到开多仓信号')
            self.logger.info('创建开多仓订单成功，开仓数量%d'%order.amount_total)
            while order.amount > 0:
                price = self._market_data.ask1 if self._slippage else self._market_data.bid1
                amount = min(order.amount, int(0.1*self._market_data.asize1))
                if amount != 0:
                    self._position += amount
                    self._position_cost += amount * price * self._scaler
                    profit = -1 * amount * price * self._scaler * self._commission_rate
                    self._account += profit
                    order.update_time = self._market_data.time
                    order.amount_traded += amount
                    self.logger.info('开仓数量%d，开仓价格%.2f，开仓收益%.2f，当前总仓位%d，当前总资产%.2f，当前可用资金%.2f'%(
                        amount, price, profit, self._position, self._account, self.available))
                    self._trade_hist.append((self._market_data.time, 'long', amount, price, self._position, self._account))
                self.read_next_tick(ticks)
        else: # sell
            amount = self.available // (self._market_data.price * self._scaler * (1 + self._commission_rate))
            if amount == 0: return
            order  = MarketOrder(amount, self._market_data.time)
            self.logger.info('收到开空仓信号')
            self.logger.info('创建开空仓订单成功，开仓数量%d'%order.amount_total)
            while order.amount > 0:
                price  = self._market_data.bid1 if self._slippage else self._market_data.price
                amount = min(order.amount, int(0.1*self._market_data.bsize1))
                if amount != 0:
                    self._position -= amount
                    self._position_cost += amount * price * self._scaler
                    profit = -1 * amount * price * self._scaler * self._commission_rate
                    self._account += profit
                    order.update_time = self._market_data.time
                    order.amount_traded += amount
                    self.logger.info('开仓数量%d，开仓价格%.2f，开仓收益%.2f，当前总仓位%d，当前总资产%.2f，当前可用资金%.2f'%(
                        amount, price, profit, self._position, self._account, self.available))
                    self._trade_hist.append((self._market_data.time, 'short', amount, price, self._position, self._account))
                self.read_next_tick(ticks)
                
    def read_next_tick(self, ticks, ref_time=None):
        while True:
            line = ticks.readline()
            if not line: return False
            feed = Feed(*line.strip().split(','))
            if feed.ask1 == 0 or feed.bid1 == 0 or feed.price == 0: continue
            self._market_data = feed
            if ref_time is None: return True
            if self._market_data.time > ref_time: return True

    def trade_orders(self, orders):
        # load ticks
        date = orders.index[0]
        code = orders.code.iloc[0]
        tick_file = os.path.join(env.TICK_PATH, date, code+'.csv')
        if not os.path.exists(tick_file):
            self.logger.warn('找不到合约%s在日期%s的tick数据'%(code, date))
            return
        # trade
        with open(tick_file, 'r') as ticks:
            ticks.readline() # skip header
            for _, signal in orders.iterrows():
                self.check_close(signal, ticks)
                self.check_open(signal, ticks)
            signal = pd.Series({
                'time': self._market_data.time,
                'long': -1,
                'short': -1
            })
            self.check_close(signal, ticks)

    def submit(self, fname):
        orders = pd.read_csv(fname, index_col='date')
        orders.index = orders.index.astype(str)
        orders.time = pd.to_datetime(orders.time)
        self.orders = orders
        calendar = sorted([x for x in os.listdir(env.TICK_PATH) if re.match(r'^[0-9]{8}$', x)])
        calendar = [x for x in calendar if orders.index[0]<=x<=orders.index[-1]]
        self.calendar = calendar

    def trade(self):
        for date in self.calendar:
            self.logger.info('当前交易日: %s'%date)
            if date in self.orders.index:
                orders = self.orders.loc[date]
                self.trade_orders(orders)
            self.logger.info('订单完成，总资产%.2f，总仓位%d，可用资金%.2f'%(
                self._account, self._position, self.available))
            self._account_hist.append(self._account)
            self._market_data = None

    def report(self):
        returns = pd.Series(self._account_hist).pct_change().fillna(0).values
        plot_chart(self.calendar, returns, self._notebook_mode)

    def get_account_history(self):
        return pd.DataFrame({
            'date': self.calendar,
            'account': self._account_hist,
        })

    def get_trade_history(self):
        return pd.DataFrame(
            self._trade_hist,
            columns='time,action,amount,price,position,account'.split(',')
        )

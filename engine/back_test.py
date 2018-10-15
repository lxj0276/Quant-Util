from collections import OrderedDict
from copy import deepcopy

from engine.assets import stock, asset
from engine.carlender import carlender_daily
from engine.engines import market_engine, asset_engine_map
from engine.graph import plot_charts_with_market_value
from engine.orders import generate_orders_from_positions
from engine.position import position
from engine.session import session_based
from engine.time_manager import Time_manager_session, Time_manager
from engine.utils import get_calendar
import pandas as pd


def merge_dict(dict1, dict2):
    result = OrderedDict()
    for k, v in dict1.items():
        if k not in result.keys():
            result[k] = v
        else:
            result[k] += v
    for k, v in dict2.items():
        if k not in result.keys():
            result[k] = v
        else:
            result[k] += v
    return result


def find_most_recent(value, value_ordereddict):
    current = None
    for k, v in value_ordereddict.items():
        if k <= value:
            current = v
        else:
            return current
    return v


class BackTest(session_based):
    def __init__(self, carlender, asset_field=[stock], initial_capital=1000000, tax_rate_and_commission=0.002):
        """warning! carlender must be sorted"""
        session = Time_manager_session(Time_manager(carlender=carlender))
        super(BackTest, self).__init__(session)
        self.carlender = carlender
        self.session.set_time(carlender.first_time())
        with self.session.as_default():
            self.current_pisition = position(init_cash=initial_capital)
            self.market_engine = market_engine()
            for asset_type in asset_field:
                self.market_engine.set_engine(asset_type, asset_engine_map[asset_type]())
            self.pre_load()
        self.position_log = OrderedDict()
        self.market_value = OrderedDict()

    def pre_load(self):
        """method to be overwrite to preload data or feature """
        raise NotImplemented()

    def generate_trade_carlender(self):
        """method to be overwrite to generate the actual trade carlender (days that contain orders)"""
        self.trade_carlender = self.carlender

    def _generate_position_percent(self):
        target_position_percent = self.generate_position_percent()
        for key in target_position_percent.keys():
            assert issubclass(type(key), asset)
        return target_position_percent

    def generate_position(self):
        target_position_percent = self._generate_position_percent()
        target_position = self.market_engine.to_target_percent(self.current_pisition, target_position_percent)
        return target_position

    def generate_carlender_marketvalues(self):
        """ call when backtest finished"""
        carlender_market_values = OrderedDict()
        for thetime in self.carlender:
            self.session.set_time(thetime)
            position = find_most_recent(thetime, self.position_log)
            if position is None:
                carlender_market_values[thetime] = self.initial_capital
            else:
                carlender_market_values[thetime] = self.market_engine.calculate_market_value(position)
        return carlender_market_values

    def back_test(self):
        with self.session.as_default():
            for current_time in self.trade_carlender:
                """use tmp to catch internal positions"""
                tmp_position = deepcopy(self.current_pisition)

                self.session.set_time(current_time)
                target_position = self.generate_position()
                orders_to_apply = generate_orders_from_positions(older_position=self.current_pisition,
                                                                 new_position=target_position)
                for order in orders_to_apply:
                    self.current_pisition.check_order(order)
                    tmp_position = self.market_engine.apply_order(order, tmp_position)
                self.position_log[current_time] = tmp_position
                self.current_pisition = tmp_position


class BackTestOrders(session_based):
    def __init__(self, pred_orders, asset_field=[stock],trade_calendar=None, initial_capital=1000000, tax_rate_and_commission=0.002,
                 benchmark='SH000300'):
        """warning! carlender must be sorted"""
        self.pred = pred_orders
        self.benchmark = benchmark
        self.initial_capital=initial_capital
        start_time = self.pred['datetime'].min()
        end_time = self.pred['datetime'].max()
        print('start backtest "{}-{}"'.format(start_time, end_time))
        all_calendar = get_calendar()
        dates = [date for date in all_calendar if date >= start_time and date <= end_time]
        carlender = carlender_daily(dates)
        session = Time_manager_session(Time_manager(carlender=carlender))
        super(BackTestOrders, self).__init__(session)
        self.carlender = carlender
        self.session.set_time(carlender.first_time())
        with self.session.as_default():
            self.current_pisition = position(init_cash=initial_capital)
            self.market_engine = market_engine()
            for asset_type in asset_field:
                self.market_engine.set_engine(asset_type, asset_engine_map[asset_type]())
            self.pre_load()
            if trade_calendar:
                self.generate_trade_carlender(trade_calendar)
            else:
                self.trade_carlender = carlender
        self.position_log = OrderedDict()
        self.market_value = OrderedDict()

    def pre_load(self):
        """method to be overwrite to preload data or feature """
        pass

    def generate_trade_carlender(self,trade_calendar):
        """method to be overwrite to generate the actual trade carlender (days that contain orders)"""
        self.trade_carlender = trade_calendar

    def generate_carlender_marketvalues(self,plot=False):
        """ call when backtest finished"""
        carlender_market_values = OrderedDict()
        for thetime in self.carlender:
            self.session.set_time(thetime)
            position = find_most_recent(thetime, self.position_log)
            if position is None:
                carlender_market_values[thetime] = self.initial_capital
            else:
                carlender_market_values[thetime] = self.market_engine.calculate_market_value(position)
        if plot:
            self.plot(pd.Series(carlender_market_values))
        return carlender_market_values



    def _generate_position_percent(self):
        target_position_percent = self.generate_position_percent()
        for key in target_position_percent.keys():
            assert issubclass(type(key), asset)
        return target_position_percent

    def generate_position_percent(self):
        position_percent = OrderedDict()
        orders = self.pred[self.pred['datetime'] == self.session.get_time()]

        ############iterrows is very slow
        for i, row in orders.iterrows():
            position_percent[stock(row['instrument_id'])] = row['position']
        return position_percent

    def generate_position(self):
        target_position_percent = self._generate_position_percent()
        target_position = self.market_engine.to_target_percent(self.current_pisition, target_position_percent)
        return target_position

    def back_test(self):
        with self.session.as_default():
            for current_time in self.trade_carlender:
                """use tmp to catch internal positions"""
                tmp_position = deepcopy(self.current_pisition)

                self.session.set_time(current_time)
                target_position = self.generate_position()
                orders_to_apply = generate_orders_from_positions(older_position=self.current_pisition,
                                                                 new_position=target_position)
                for order in orders_to_apply:
                    self.current_pisition.check_order(order)
                    tmp_position = self.market_engine.apply_order(order, tmp_position)
                self.position_log[current_time] = tmp_position
                self.current_pisition = tmp_position
            self.market_value = pd.Series(self.generate_carlender_marketvalues())


    def plot(self,market_value=None):
        if not (market_value is None ):
            plot_charts_with_market_value(market_values=market_value, benchmark=self.benchmark)
        else:
            plot_charts_with_market_value(market_values=self.market_value, benchmark=self.benchmark)


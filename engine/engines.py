import numpy as np

from abc import ABC, abstractmethod
from collections import OrderedDict
from global_data_loader.data_memory_cache import PY_CACHE
from engine.assets import asset, stock, cash
from engine.cons import *
from engine.data_base import PRICING_DATA_STOCK
from engine.data_loader import pricing_data_loader
from engine.env import TRADE_COST
from engine.errors import ENGINE_NOT_FOUND_ERROR
from engine.session import session_based
from engine.utils import generate_all_like_1d


def SET_TRADE_COST(trade_cost):
    global TRADE_COST
    TRADE_COST = trade_cost


def GET_TRADE_COST():
    return TRADE_COST

class asset_engine(session_based, ABC):
    def __init__(self, asset_type, session=None):
        super(asset_engine, self).__init__(session)
        assert issubclass(asset_type, asset)
        self._asset_type = asset_type

    def is_engine(self, asset):
        if self._asset_type == asset:
            return True
        else:
            return False

    @property
    def asset_type(self):
        return self._asset_type

    @abstractmethod
    def load_marketing_data(self, pricing_data_dict):
        raise NotImplemented()

    @abstractmethod
    def apply_order(self, order, position):
        raise NotImplemented()

    @property
    def asset_type(self):
        return self._asset_type


class stock_engine(asset_engine):
    def __init__(self, session=None):
        super(stock_engine, self).__init__(stock, session)
        self.global_data = PY_CACHE.get_data()

        if not hasattr(self.global_data, CACHE_STOCKS):
            setattr(self.global_data, CACHE_STOCKS, set())
        self.data_loader = pricing_data_loader()
        for KEY in STOCK_PRICING_DATA_KEY:
            if not hasattr(self.global_data, KEY):
                setattr(self.global_data, KEY, PRICING_DATA_STOCK(KEY, session=self.session))
            else:
                getattr(self.global_data, KEY).reset_session(self.session)

    def load_marketing_data(self, pricing_data_dict):
        """pricing_data_dict should be a session_based data object"""
        for KEY in STOCK_PRICING_DATA_KEY:
            assert pricing_data_dict[KEY].session == self.session
            setattr(self.global_data, KEY, pricing_data_dict[KEY])

    def check_and_load_asset(self, asset_instance):
        if asset_instance not in getattr(self.global_data, CACHE_STOCKS):
            ################################################################文件格式原因↓
            pricing_data,on_trading=self.data_loader.load_single_data(asset_instance.ID,
                                                                      self.session.get_calendar().first_time(),
                                                                      self.session.get_calendar().last_time()+1)
            # pricing_data, on_trading = self.data_loader.load_single_data(asset_instance.ID,
            #                                                              self.session.get_calendar().first_time(),
            #                                                              self.session.get_calendar().last_time())
            getattr(self.global_data, PRICE).set_asset_instance_data(asset_instance, pricing_data)
            getattr(self.global_data, ON_TRADING).set_asset_instance_data(asset_instance, on_trading)
            getattr(self.global_data, IS_LIMITDOWN).set_asset_instance_data(asset_instance,
                                                                            generate_all_like_1d(on_trading, 0))
            getattr(self.global_data, IS_LIMITUP).set_asset_instance_data(asset_instance,
                                                                          generate_all_like_1d(on_trading, 0))
            getattr(self.global_data, CACHE_STOCKS).add(asset_instance)

    def apply_order(self, order, position):
        # position=deepcopy(position)
        self.check_and_load_asset(order.asset_instance)
        current_price = getattr(self.global_data, PRICE).get_data(order._asset_instance)
        if order.direction_flag == BID:
            bid_amount = min(order.order_volme, position.get_cash() // (current_price * (1 + TRADE_COST)),
                             0 if not getattr(self.global_data, ON_TRADING).get_data(order._asset_instance) else np.inf,
                             0 if getattr(self.global_data, IS_LIMITUP).get_data(order._asset_instance) else np.inf)
            if bid_amount == 0:
                return position

            cash_consume = bid_amount * current_price * (1 + TRADE_COST)
            position.add_asset(order._asset_instance, bid_amount)
            position.reduce_cash(cash_consume)
            return position
        elif order.direction_flag == ASK:
            ask_amount = min(order._order_volume,
                             0 if not getattr(self.global_data, ON_TRADING).get_data(order._asset_instance) else np.inf,
                             0 if getattr(self.global_data, IS_LIMITDOWN).get_data(order._asset_instance) else np.inf)
            if ask_amount == 0:
                return position
            cash_gain = ask_amount * current_price
            position.reduce_asset(order._asset_instance, ask_amount)
            position.add_cash(cash_gain)
        return position

    def calculate_market_value(self, asset_instance, amount):
        self.check_and_load_asset(asset_instance)
        return getattr(self.global_data, PRICE).get_data(asset_instance) * amount

    def get_price(self, asset_instance):
        self.check_and_load_asset(asset_instance)
        return getattr(self.global_data, PRICE).get_data(asset_instance)


class market_engine(session_based):
    def __init__(self, session=None):
        super(market_engine, self).__init__(session)
        self.asset_engine_dict = dict()

    def set_engine(self, _asset_type, asset_engine_):
        assert asset_engine_.is_engine(_asset_type)
        assert issubclass(_asset_type, asset)
        ##存储engine
        self.asset_engine_dict[_asset_type] = asset_engine_

    def find_engine(self, asset_type):
        if asset_type not in self.asset_engine_dict.keys():
            raise ENGINE_NOT_FOUND_ERROR('engine for {} not found in market_engine'.format(asset_type))
        else:
            return self.asset_engine_dict[asset_type]

    def apply_order(self, order, position):
        engine_to_apply = self.find_engine(order.asset_type)
        newposition = engine_to_apply.apply_order(order, position)
        return newposition

    def calculate_market_value(self, position):
        market_value = 0
        cash_ = 0
        for asset_instance, amount in position.items():
            if type(asset_instance) == cash:
                cash_ = amount
                continue
            market_value += self.find_engine(asset_instance.asset_type).calculate_market_value(asset_instance, amount)
        return market_value + cash_

    def asset_pricing(self, asset_instance):
        engine_to_apply = self.find_engine(asset_instance.asset_type)
        return engine_to_apply.get_price(asset_instance)

    def max_amout_can_ask(self, asset_instance, position):
        pass

    def max_amount_can_bid(self, asset_instance, position):
        pass

    def to_target_percent(self, position, target_percent_position):
        has_cash = False
        target_position = OrderedDict()
        market_value = self.calculate_market_value(position)
        for k, v in target_percent_position.items():
            if isinstance(k, cash):
                cash_ = k
                has_cash = True
                continue
            if self.asset_pricing(k) == self.asset_pricing(k):
                target_position[k] = (v * market_value) // self.asset_pricing(k)

        if has_cash:
            target_position[cash_] = market_value - self.calculate_market_value(target_position)
        return target_position


asset_engine_map = {stock: stock_engine}

if __name__ == '__main__':
    from engine.time_manager import Time_manager, Time_manager_session
    from engine.carlender import carlender_daily
    import pandas as pd
    from engine.utils import try_to_parse_date

    dates = list(map(try_to_parse_date, pd.date_range('2017-08-01', '2017-09-01').to_pydatetime()))
    carlender = carlender_daily(dates)
    dates[9]
    carlender.first_time()
    session_ = Time_manager_session(Time_manager(carlender=carlender))
    se = stock_engine(session=session_)
    session_.set_time(session_.time_manager.carlender.first_time())
    se.get_price(stock('CN_STK_SH600233'))
    mg = market_engine(session=session_)
    mg.set_engine(stock, se)
    mg.asset_pricing(stock('CN_STK_SH600009'))

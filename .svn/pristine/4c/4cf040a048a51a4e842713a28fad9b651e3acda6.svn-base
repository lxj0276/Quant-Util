from collections import OrderedDict

from engine.carlender import carlender_daily
from engine.engines import market_engine, stock_engine
from engine.orders import generate_orders_from_positions
from engine.position import position
from engine.time_manager import Time_manager_session, Time_manager
from engine.utils import get_calendar, get_next_calendar, max_drop_down
from strategy_playground.cons import INIT_CASH
from tqdm import tqdm


class metric(market_engine):
    def __init__(self, start_time=None, end_time=None):
        session = Time_manager_session(
            time_manager=Time_manager(carlender=carlender_daily(get_calendar(start_time, end_time))))
        super(metric, self).__init__(session)

    def evaluate_proposal(self, proposal):
        pass

    def evaluate(self, proposals):
        pass


class accum_return(metric):
    def evaluate_return(self, proposals):
        calendar = proposals.keys()
        thereturn = OrderedDict()
        tmp_position = position(init_cash=INIT_CASH)
        orderdict = OrderedDict()
        for trade_date in tqdm(calendar, desc='accum_return'):
            self.session.set_time(trade_date)
            target_position = self.to_target_percent(tmp_position, proposals[trade_date])
            orders_to_apply = generate_orders_from_positions(tmp_position, target_position)
            orderdict[trade_date] = orders_to_apply
            for order in orders_to_apply:
                tmp_position = self.apply_order(order, tmp_position)

            self.session.set_time(get_next_calendar(trade_date, get_calendar()))
            thereturn[trade_date] = self.calculate_market_value(tmp_position) / INIT_CASH
        return thereturn, orderdict

    def evaluate(self, proposals):
        thereturn, orderdict = self.evaluate_return(proposals)
        return thereturn.popitem()[1]


class max_withdraw(metric):
    def __init__(self, start_time=None, end_time=None):
        super(max_withdraw, self).__init__(start_time, end_time)
        self.acc = accum_return()

    def evaluate(self, proposals):
        thereturn, orderdict = self.acc.evaluate_return(proposals)
        mdd, _t = max_drop_down(thereturn.values)
        return mdd


if __name__ == '__main__':
    stockId = 'CN_STK_SH600104'
    from strategy_playground.invest_proposal import proposal_percentage, single_proposal_percentage
    from engine.assets import stock

    calendar = get_calendar(20170101, 20171101)
    p = proposal_percentage()
    for date in calendar:
        p.add_poposal(date, single_proposal_percentage(date, {stock(stockId): 0.8}))
    c = accum_return()

    c.set_engine(stock, stock_engine(session=c.session))
    print(c.evaluate_return(p))

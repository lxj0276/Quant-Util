import os
import random
from abc import abstractmethod
from collections import OrderedDict

import xarray as xr
from datetime import datetime
from engine.assets import stock
from engine.engines import stock_engine
from engine.session import session_based
from engine.time_manager import Time_manager_session
from engine.utils import get_calendar
from feature import *
from feature.ops import *
from quantlab_utils.persistent import read_obj, write_obj
from quantlab_utils.utils import time_shift, get_calendar
from strategy_playground.cons import *
from strategy_playground.invest_proposal import proposal_percentage, single_proposal_percentage
from strategy_playground.metrics import accum_return
from tqdm import tqdm


class base_strategy(session_based):
    def __init__(self, stock_universe=None, name=None):
        self.stock_universe = stock_universe
        super(base_strategy, self).__init__(Time_manager_session())
        self._preloaded = False
        self._name = name
        self.proposal_cache_path = os.path.join(STRATEGE_CACHE_PATH, self.name, PROPOSAL)
        self._load_proposal_from_cache()

    def clear_cache(self):
        if os.path.exists(self.proposal_cache_path):
            os.remove(self.proposal_cache_path)

    def _load_proposal_from_cache(self):
        if os.path.exists(self.proposal_cache_path):
            self.proposal_cache = read_obj(self.proposal_cache_path)
        else:
            self.proposal_cache = proposal_percentage()

    def _save_cache(self):
        """
        derived class overwrite this method to do cache

        :return:
        """
        write_obj(self.proposal_cache, self.proposal_cache_path)

    def _preload(self):
        """

        :return:
        """
        if self._preloaded:
            return
        preload, startime, endtime = self.preload()
        self.preload_features = preload
        startime = startime if startime else 20120101
        endtime = endtime if endtime else int(datetime.now().strftime('%Y%m%d'))
        if preload is not None:
            self.cache = load_dataset(self.stock_universe, preload, TimeRange(startime, endtime), return_xarray=True)
        self.preload_start_time = startime
        self.preload_end_time = endtime
        self._preloaded = True

    def preload(self):
        """
        this method is to be written by users to give the strategy begin&endtime
        :return:preload features,begin_time,end_time
        """
        return [], None, None

    @property
    def _classname(self):
        return type(self).__name__

    @property
    def name(self):
        if hasattr(self, '_name'):
            if getattr(self, '_name') is not None:
                return getattr(self, '_name')
        if '__' in self._classname:
            return ''.join(self._classname.split('__')[:-1])
        return self._classname

    def load_dataset(self, features, window=15, date=None):
        self._preload()
        if date == None:
            date = self.session.get_time()
        start_time = time_shift(date, window)
        cached_feature = [feature.get_name() for feature in features if feature in self.preload_features]
        not_cached_feature = [feature for feature in features if feature not in self.preload_features]
        cached = self.cache.sel(datetime=slice(start_time, date), feature=cached_feature) if len(
            cached_feature) > 0 else None
        not_cached = load_dataset(self.stock_universe, not_cached_feature, TimeRange(start_time, date + 1),
                                  return_xarray=True) if len(not_cached_feature) > 0 else None
        if cached is None:
            return not_cached
        elif not_cached is None:
            return cached
        else:
            result = xr.concat([cached, not_cached], dim='feature')
            return result

    def generate_proposal(self, carlendar, overwrite=True):
        proposal = proposal_percentage()
        for date in tqdm(carlendar, desc='generate_proposal'):
            proposal.add_poposal(date, self.__generate_single_proposal(date))
        if overwrite:
            self._save_cache()
        return proposal

    def __generate_single_proposal(self, date):
        if date in self.proposal_cache.keys():
            return self.proposal_cache[date]
        else:
            proposal_ = self._generate_single_proposal(date)
            self.proposal_cache.add_poposal(date, proposal_)
            return proposal_

    def back_test(self, start_time, end_time):
        carlendar = get_calendar(start_time, end_time)
        self._preload()
        if not hasattr(self, 'c'):
            c = accum_return()
        else:
            c = getattr(self, 'c')
        c.set_engine(stock, stock_engine(session=c.session))
        # print(c.evaluate_return(s.generate_proposal(calendar)))
        proposals = self.generate_proposal(carlendar)
        market_value, order = c.evaluate_return(proposals)
        market_value = pd.Series(market_value)
        # plot_charts_with_market_value(market_value, benchmark='SH000300')
        return market_value, order

    @abstractmethod
    def _generate_single_proposal(self, date):
        pass


class naive_average_strategy(base_strategy):
    def from_stockIds_to_proposal(self, stockIds):
        length = len(stockIds)
        single_proposal = single_proposal_percentage()
        for stockId in stockIds:
            single_proposal.add_proposal(stock(stockId), 1 / length)
        return single_proposal

    @abstractmethod
    def generate_single_proposal(self, date):
        df = self.load_dataset([Close_Daily(), EMA5_Daily()], 10, date)
        stockId = [random.choice(df.instrument_id.tolist())]
        return stockId

    def _generate_single_proposal(self, date):
        stockIds = self.generate_single_proposal(date)
        return self.from_stockIds_to_proposal(stockIds)


class score_strategy(base_strategy, Feature):
    def __init__(self, stock_universe, topk, name=None):
        super(score_strategy, self).__init__(stock_universe=stock_universe, name=name)
        self.topk = topk
        self._score_cache_path = os.path.join(STRATEGE_CACHE_PATH, self.name, SCORE)
        self._load_score_from_cache()

    def _load_score_from_cache(self):
        if os.path.exists(self._score_cache_path):
            self.score_cache = read_obj(self._score_cache_path)
        else:
            self.score_cache = dict()

    def _save_cache(self):
        super(score_strategy, self)._save_cache()
        write_obj(self.score_cache, self._score_cache_path)

    def clear_cache(self):
        super(score_strategy, self).clear_cache()
        if os.path.exists(self._score_cache_path):
            os.remove(self._score_cache_path)

    @abstractmethod
    def generate_score(self, date):
        pass

    def get_score(self, date):
        if date in self.score_cache.keys():
            scores = self.score_cache[date]
        else:
            scores = self.generate_score(date).sort_values(ascending=False)
            scores.name = date
            self.score_cache[date] = scores
        return scores

    def group_backtest(self, calendar, n_group=3):
        # TODO: add group backtest curve&statistics
        pass

    def _load_feature(self, instrument_ids, time_range):
        calendar = get_calendar(time_range.begin_time, time_range.end_time)
        scores_list = []
        for date in calendar:
            scores_list.append(self.get_score(date))
        df = pd.concat(scores_list, axis=1)
        df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
        df = df[df.instrument_id.isin(instrument_ids)]
        return df

    def _create_feature(self, instrument_id, time_range):
        # time_range will be removed in the future
        return self._load_feature(instrument_id, time_range)

    def _generate_single_proposal(self, date):
        scores = self.get_score(date)
        stockIds = scores.head(self.topk).index
        proposal = single_proposal_percentage()
        for stockId in stockIds:
            proposal.add_proposal(stock(stockId), 1 / len(stockIds))
        return proposal


if __name__ == "__main__":
    from feature import *
    from feature.ops import *


    class m(base_strategy):
        def preload(self):
            preload_ = [Open_Daily(), Close_Daily()]
            return preload_, 20170101, 20171201


    preload = [Open_Daily(), Close_Daily()]
    features = [Open_Daily(), Close_Daily(), High_Daily(), Vol_Daily()]
    instrument_ids = list_instrument_ids(instrument_type='STK')
    s = m(instrument_ids[:100])
    s._preload()
    df = s.load_dataset(features, 15, date=20171108)
    self = s
    startime = 20170101
    endtime = 20170601
    self.preload_start_time = startime
    self.preload_end_time = endtime
    self.preload_features = preload

    if preload is not None:
        self.cache = load_dataset(self.stock_universe, preload, TimeRange(startime, endtime), return_xarray=True)

    backward_length = 15
    current_time = 20170526
    start_time = time_shift(current_time, backward_length)
    cached_feature = [feature.get_name() for feature in features if feature in self.preload_features]
    not_cached_feature = [feature for feature in features if feature not in self.preload_features]
    cached = self.cache.sel(datetime=slice(start_time, current_time))
    not_cached = load_dataset(self.stock_universe, not_cached_feature, TimeRange(start_time, current_time + 1),
                              return_xarray=True)
    result = xr.concat([cached, not_cached], dim='feature').shape

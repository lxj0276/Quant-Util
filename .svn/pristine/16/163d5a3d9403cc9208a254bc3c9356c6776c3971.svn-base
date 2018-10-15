from abc import ABC, abstractmethod

from engine.assets import stock
from engine.session import session_based
from engine.utils import try_to_parse_date


class DataBase(session_based, ABC):
    def __init__(self, session=None):
        super(DataBase, self).__init__(session)
        self.data = dict()

    @abstractmethod
    def _load_data(self, datasource):
        pass

    def reset_session(self, session):
        self.session = session


class DfFeature(DataBase):
    def __init__(self, datasource, session=None):
        super(DfFeature, self).__init__(session)
        self._load_data(datasource)

    def _load_data(self, datasource):
        """data source must have thetime columns"""
        import pandas as pd
        if not isinstance(datasource, pd.DataFrame):
            raise TypeError('DfFeature must loaded from pd.DataFrame')
        self.data = datasource
        self.data['thetime'] = self.data['thetime'].apply(lambda x: try_to_parse_date(x))

    def _filter(self, data):
        current_time = self.session.time_manager.get_current_time()
        return data[data['thetime'] < current_time]

    def get_data(self):
        return self._filter(self.data)


class PRICING_DATA_STOCK(DataBase):
    def __init__(self, name, session=None, datasource=None, form_organized=False):
        self.name = name
        super(PRICING_DATA_STOCK, self).__init__(session)
        if not (datasource is None):
            self._load_data(datasource, form_organized)

    def get_data(self, asset_instance, thetime=None):
        if thetime is None:
            thetime = self.session.get_time()
        return self.data[asset_instance][thetime]

    def _load_data(self, datasource, form_organized=False):
        """datasource should be stockId(str):calender(datetime.date):data recursive dict"""
        if form_organized:
            self.data = datasource
            return

        for stockId, values in datasource.items():
            for thetime, inner_data in values.items():
                self.data[stock(stockId)][thetime] = inner_data

    def set_asset_instance_data(self, asset_instance, data):
        self.data[asset_instance] = data


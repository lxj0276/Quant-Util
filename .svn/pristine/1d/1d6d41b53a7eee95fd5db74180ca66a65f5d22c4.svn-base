from feature.base import OperatorFeature
from engine.utils import get_calendar
class Shift_Skipna(OperatorFeature):
    def __init__(self, feature, period):
        self.feature = feature
        self.period = period

    def __str__(self):
        return '{}({}, {})'.format(
            self.name, self.feature, self.period)

    def _load_feature(self, instrument_id, time_range):
        series = self.feature.load(instrument_id, time_range.shift(100))
        for col in series.columns:
            series[col]=series[col].dropna().shift(self.period).reindex(series.index).fillna(method='ffill')
        series = series.loc[time_range.begin_time:time_range.end_time - 1]
        return series

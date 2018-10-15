from feature.base import PersistentFeature
from feature.ops import *
from feature.zoo.Close_Daily import Close_Daily


class MA20_Daily(PersistentFeature):
    description = '20-day moving average of daily close price feature'

    granularity = 'day'

    def _create_feature(self, instrument_id, time_range):
        return MA_skipna(Close_Daily(), 20).load(instrument_id, time_range)


if __name__=='__main__':
    from feature import *
    from feature.ops import *
    instrument_ids = ['CN_STK_SH600000', 'CN_STK_SH600016', 'CN_STK_SH600019', 'CN_STK_SH600028', 'CN_STK_SH600029',
                 'CN_STK_SH600030', 'CN_STK_SH600036'
        , 'CN_STK_SH600048', 'CN_STK_SH600050', 'CN_STK_SH600104', 'CN_STK_SH600111', 'CN_STK_SH600309',
                 'CN_STK_SH600340', 'CN_STK_SH600518',
                 'CN_STK_SH600519', 'CN_STK_SH600547', 'CN_STK_SH600606', 'CN_STK_SH600837', 'CN_STK_SH600887',
                 'CN_STK_SH600919', 'CN_STK_SH600958',
                 'CN_STK_SH600999', 'CN_STK_SH601006', 'CN_STK_SH601088', 'CN_STK_SH601166', 'CN_STK_SH601169',
                 'CN_STK_SH601186', 'CN_STK_SH601211',
                 'CN_STK_SH601229', 'CN_STK_SH601288', 'CN_STK_SH601318', 'CN_STK_SH601328', 'CN_STK_SH601336',
                 'CN_STK_SH601390', 'CN_STK_SH601398',
                 'CN_STK_SH601601', 'CN_STK_SH601601', 'CN_STK_SH601628', 'CN_STK_SH601668', 'CN_STK_SH601669',
                 'CN_STK_SH601688', 'CN_STK_SH601766',
                 'CN_STK_SH601800', 'CN_STK_SH601857', 'CN_STK_SH601878', 'CN_STK_SH601881', 'CN_STK_SH601985',
                 'CN_STK_SH601988', 'CN_STK_SH601989', 'CN_STK_SH603993'
                 ]

    time_range=TimeRange(20130101,20171001)
    clo=Close_Daily()
    series = CLO.load(instrument_id, time_range.shift(20))
    series = series.rolling(20).mean()
    series = series.iloc[20:]
    MA20_Daily()._create_feature(instrument_id, time_range)
    MA(Close_Daily(), 20).load(instrument_id, time_range)
    MA(Close_Daily(), 20)._load_feature(instrument_id, time_range)

    skip_suspend = get_option('skip_suspend', False)
    series = MA(Close_Daily(), 20)._load_feature(instrument_id, time_range)
    for instrument_id in instrument_ids:
        if instrument_id not in series.columns:
            series[instrument_id] = np.nan
    series = series[instrument_ids]
    setattr(series, '__name', str(self))
    # series=series.rename(columns={series.columns[0]:str(self)})
    # series=series[str(self)]
    # series.name=self.get_name()
    # handle suspend period
    if skip_suspend:
        series = series.dropna()

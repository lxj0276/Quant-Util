from datetime import datetime, timedelta
from engine.utils  import get_calendar
from feature.env import MONGO_CONN
from mongoapi.get_data import getData, getDataForIndustry
from engine.utils import get_calendar


def time_shift_normal(thetime, shift_num):
    thetime = datetime.strptime(str(thetime), '%Y%m%d')
    thetime -= timedelta(days=shift_num)
    return int(thetime.strftime('%Y%m%d'))

def time_shift(thetime,shift_num):
    calendar=get_calendar()
    thetime_index=calendar.index(thetime)
    return calendar[max(0,thetime_index-shift_num)]


class industry:
    stock_industry_dict=dict()
    industry_stock_dict=dict()
    __loaded=None

    @classmethod
    def get_proposal_daily_return(cls, proposal, date):
        proposal_daily_return = [  percentage*cls.get_stock_daily_return(stockID, date) for stockID,percentage in proposal.items() ]
        return sum(proposal_daily_return)

    @classmethod
    def get_proposal_industry_daily_return(cls, proposal, date):
        '''
        :param proposal: dict {stockID: stockPercentage}
        :param start_time:
        :param end_time:
        :return: proposal return in industry view
        '''
        proposal_industry = {}
        for stockID, percentage in proposal.items():
            stockID_industry = cls.get_industry(stockID)
            if stockID_industry in proposal_industry:
                proposal_industry[stockID_industry] += percentage
            else:
                proposal_industry[stockID_industry] = percentage
        proposal_industry_daily_return = [percentage * cls.get_industry_daily_return(industryID, date) for industryID, percentage in proposal_industry.items()]
        return sum(proposal_industry_daily_return)

    @classmethod
    def get_proposal_range_return(cls,proposal, start_time,end_time):
        # fixed proposal
        dayRange = get_calendar(start_time, end_time)
        return_list = [(date, cls.get_proposal_daily_return(proposal, date)) for date in dayRange]
        return return_list

    @classmethod
    def get_proposal_industry_range_return(cls,proposal, start_time,end_time):
        # fixed proposal
        dayRange = get_calendar(start_time, end_time)
        return_list = [(date, cls.get_proposal_industry_daily_return(proposal, date)) for date in dayRange]
        return return_list

    @classmethod
    def get_proposal_list_range_return(cls, proposal_list):
        '''
        :param proposal_list: list of (date, date_proposal), date_proposal is the dict{stockID:percentage}
        :return: proposal_return, proposal_industry_return
        '''
        proposal_return = [ (date, cls.get_proposal_daily_return(proposal, date)) for (date, proposal) in proposal_list ]
        proposal_industry_return = [ (date, cls.get_proposal_industry_daily_return(proposal, date)) for (date, proposal) in proposal_list ]

        return proposal_return, proposal_industry_return


    @classmethod
    def plot_proposal_industry_range_return_offline(cls, proposal, start_time, end_time):
        # for fixed proposal
        dayRange = get_calendar(start_time, end_time)
        proposal_return = cls.get_proposal_range_return(proposal, start_time, end_time)
        proposal_industry_return = cls.get_proposal_industry_range_return(proposal, start_time, end_time)
        cls.plot_proposal(dayRange, proposal_return, proposal_industry_return)

    @classmethod
    def plot_proposal_list_range_return_offline(cls, proposal_list):
        # for flexible proposal
        dayRange = [node[0] for node in proposal_list]
        proposal_return, proposal_industry_return = cls.get_proposal_list_range_return(proposal_list)
        cls.plot_proposal(dayRange, proposal_return, proposal_industry_return)

    @classmethod
    def plot_proposal(cls, dayRange, proposal_return, proposal_industry_return):
        import plotly
        from plotly.graph_objs import Scatter, Layout
        plotly.offline.init_notebook_mode(connected=True)
        # plotly
        trace1 = Scatter(
            x=['%s-%s-%s' % (str(date)[0:4], str(date)[4:6], str(date)[6:8]) for date in dayRange],
            y=[node[1] for node in proposal_return],
            name='proposal'
        )
        trace2 = Scatter(
            x=['%s-%s-%s' % (str(date)[0:4], str(date)[4:6], str(date)[6:8]) for date in dayRange],
            y=[node[1] for node in proposal_industry_return],
            name='industry'
        )
        data = [trace1, trace2]
        layout = Layout(
            title='proposal return',
            yaxis=dict(
                title='return'
            )
        )
        plotly.offline.iplot({
            "data": data,
            "layout": layout
        },
            show_link=False)


if __name__=='__main__':
    a = industry.get_industry('CN_STK_SH600104')
    print(a)
    industry.get_industry_daily_return(industryID, 20171201)
    proposal = {
        'CN_STK_SZ000957':0.8,
        'CN_STK_SZ002537':0.2
    }

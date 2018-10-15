from strategy_playground.return_utils import get_proposal_range_return, get_proposal_industry_range_return
from engine.utils import get_calendar

def cumulative_proposal_return(proposal_return):
    len_daterange = len(proposal_return)
    proposal_return_values = [ node[1] + 1 for node in proposal_return ]
    proposal_return_dayRange = [ node[0] for node in proposal_return ]
    # cumulate
    for i in range(1, len_daterange):
        proposal_return_values[i] = proposal_return_values[i] * proposal_return_values[i-1]
    return zip(proposal_return_dayRange, proposal_return_values)

def plot_proposal(proposal, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)
    proposal_return = get_proposal_range_return(proposal, start_time, end_time)
    proposal_industry_return = get_proposal_industry_range_return(proposal, start_time, end_time)
    plot_proposal_return(dayRange, proposal_return, proposal_industry_return)

def plot_proposal_cumulative(proposal, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)
    proposal_return = get_proposal_range_return(proposal, start_time, end_time)
    proposal_industry_return = get_proposal_industry_range_return(proposal, start_time, end_time)

    proposal_return = cumulative_proposal_return(proposal_return)
    proposal_industry_return = cumulative_proposal_return(proposal_industry_return)
    plot_proposal_return(dayRange, proposal_return, proposal_industry_return)


def plot_proposal_return(dayRange, proposal_return, proposal_industry_return):
    '''
    :param dayRange: list of date
    :param proposal_return: list of (date, reuturn)
    :param proposal_industry_return: list of (date, return)
    :return:
    '''
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
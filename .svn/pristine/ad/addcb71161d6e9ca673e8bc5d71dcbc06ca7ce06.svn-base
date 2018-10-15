from datetime import datetime, timedelta
from engine.utils import get_calendar
from feature.env import MONGO_CONN
from mongoapi.get_data import getData, get_stock_return, get_index_return, get_daily_proposal_value, get_daily_index_value
from quantlab_utils.industry import industry
import numpy as np


'''
def get_stock_return(instrument_ids, start_time, end_time):

'''

def get_proposal_daily_return(daily_proposal, date):
    if type(list(daily_proposal.keys())[0]) is not str:
        instrument_ids = [key.ID for key in list(daily_proposal.keys())]
        instrument_percent = {key.ID:value for key,value in daily_proposal.items()}
    else:
        instrument_ids = list(daily_proposal.keys())
        instrument_percent = daily_proposal

    start_time = date
    end_time = date+1
    return_df = get_stock_return(instrument_ids, start_time, end_time)
    daily_return = sum([ instrument_percent[instrument_id] * return_df[instrument_id].values[0] for instrument_id in instrument_ids ])
    return daily_return

def get_industry_daily_return(industry_id, date):
    instrument_ids = industry.get_stocks(industry_id)
    start_time = date
    end_time = date + 1
    return_df = get_stock_return(instrument_ids, start_time, end_time)
    daily_return = sum([return_df[instrument_id].values[0] for instrument_id in instrument_ids]) / len(instrument_ids)
    return daily_return

def get_proposal_industry_daily_return(daily_proposal, date):
    '''
    :param proposal: dict {stockID: stockPercentage}
    :param start_time:
    :param end_time:
    :return: proposal return in industry view
    '''
    if type(list(daily_proposal.keys())[0]) is not str:
        instrument_ids = [key.ID for key in list(daily_proposal.keys())]
        proposal = {key.ID: value for key, value in daily_proposal.items()}
    else:
        instrument_ids = list(daily_proposal.keys())
        proposal = daily_proposal

    proposal_industry = {}

    # generate industry proposal
    for stockID, percentage in proposal.items():
        stockID_industry = industry.get_industry(stockID)
        if stockID_industry in proposal_industry:
            proposal_industry[stockID_industry] += percentage
        else:
            proposal_industry[stockID_industry] = percentage
    proposal_industry_daily_return = sum([percentage * get_industry_daily_return(industryID, date) for industryID, percentage in proposal_industry.items()])
    return  proposal_industry_daily_return

def get_proposal_range_return(proposal, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)
    return_list = [ (date, get_proposal_daily_return(proposal[date], date)) for date in dayRange ]
    return return_list

def get_proposal_industry_range_return(proposal, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)
    return_list = [(date, get_proposal_industry_daily_return(proposal[date], date)) for date in dayRange]
    return return_list

def cumulative_proposal_return(proposal_return):
    len_daterange = len(proposal_return)
    proposal_return_values = [ node[1] + 1 for node in proposal_return ]
    proposal_return_dayRange = [ node[0] for node in proposal_return ]
    # cumulate
    for i in range(1, len_daterange):
        proposal_return_values[i] = proposal_return_values[i] * proposal_return_values[i-1]
    return list(zip(proposal_return_dayRange, proposal_return_values))

def get_proposal_range_cumulative_return(proposal, start_time, end_time):
    proposal_return = get_proposal_range_return(proposal, start_time, end_time)
    proposal_cumulative_return = cumulative_proposal_return(proposal_return)
    return proposal_cumulative_return


def get_index_range_return(indexID, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)
    index_df = get_index_return([indexID], start_time, end_time)
    return_value_list = list(index_df[indexID].values)
    return_index_list = list(index_df.index.values)
    index_range_return = list(zip(return_index_list, return_value_list))
    return index_range_return


# evaluate return
def get_proposal_shape_ratio(proposal, start_time, end_time ,benchmark=0.04):
    '''
    :param proposal:   {date:daily_proposol}
    :param benchmark: 4% as default
    :return: sharp ratio
    '''

    return_list = get_proposal_range_return(proposal, start_time, end_time)
    rate_list = np.array([node[1] for node in return_list])
    sharpe_ratio =(  ( np.mean(rate_list) - benchmark ) *250 ) / (np.std(rate_list) * np.sqrt(250))

    return sharpe_ratio

def get_max_dropdown(rate_list):
    return max( [ rate_list[i] - max(rate_list[:i])  for i in range(1, len(rate_list))] )

def get_proposal_max_dorpdown(proposal, start_time, end_time ):
    proposal_cumulative_return = get_proposal_range_cumulative_return(proposal, start_time, end_time)
    cumulative_return_list = [node[1] for node in proposal_cumulative_return]
    return get_max_dropdown(cumulative_return_list)

def get_proposal_annual_return(proposal, start_time, end_time ):
    dayRange = get_calendar(start_time, end_time)
    proposal_start = proposal[dayRange[0]]
    proposal_end = proposal[dayRange[-1]]
    value_start = get_daily_proposal_value(proposal_start, dayRange[0])
    value_end = get_daily_proposal_value(proposal_end, dayRange[-1])
    annual_return =  np.power( (value_end/ value_start) , (250/len(dayRange)) ) - 1
    return annual_return

def get_index_annual_return(indexID, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)
    value_start = get_daily_index_value(indexID, dayRange[0])
    value_end = get_daily_index_value(indexID, dayRange[-1])
    annual_return = np.power( (value_end / value_start) , (250 / len(dayRange)) ) - 1
    return annual_return

def get_proposal_Beta(proposal, start_time, end_time, indexID='CN_STK_SH000300'):
    proposal_range_return = get_proposal_range_return(proposal, start_time, end_time)
    index_range_return = get_index_range_return(indexID, start_time, end_time)
    # get value data only [ (date, return_rate) ]
    proposal_range_return = [node[1] for node in proposal_range_return]
    index_range_return = [node[1] for node in index_range_return]

    proposal_annual_return = get_proposal_annual_return(proposal, start_time, end_time )
    index_annual_return = get_index_annual_return(indexID, start_time, end_time)

    beta = np.cov(proposal_range_return, index_range_return)[0][1] / np.var(index_range_return)

    return beta

def get_proposal_Alpha(proposal, start_time, end_time, indexID='CN_STK_SH000300', risk_free_rate = 0.04):
    proposal_annual_return = get_proposal_annual_return(proposal, start_time, end_time)
    index_annual_return = get_index_annual_return(indexID, start_time, end_time)
    beta = get_proposal_Beta(proposal, start_time, end_time, indexID)
    alpha = proposal_annual_return - risk_free_rate - beta * (index_annual_return - risk_free_rate)
    return alpha

def get_proposal_return_volatility(proposal, start_time, end_time):
    dayRange = get_calendar(start_time, end_time)

    proposal_range_return = get_proposal_range_return(proposal, start_time, end_time)
    # get value data only [ (date, return_rate) ]
    proposal_range_return = [node[1] for node in proposal_range_return]
    len_dayRange = len(proposal_range_return)
    return np.sqrt( 250 * (len_dayRange / (len_dayRange-1) )* np.var(proposal_range_return) )
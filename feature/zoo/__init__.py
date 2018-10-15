from feature.zoo.MA_Daily import MA_Daily
from feature.zoo.ADX import ADX
from feature.zoo.ADX_Daily import ADX_Daily
from feature.zoo.AbnormalVolatility_Daily import AbnormalVolatility_Daily
from feature.zoo.Alpha import Alpha
from feature.zoo.AlphaHS300_Daily import AlphaHS300_Daily
from feature.zoo.Aroon import Aroon
from feature.zoo.AroonUp_Daily import AroonUp_Daily
from feature.zoo.ArronDown_Daily import AroonDown_Daily
from feature.zoo.BBI import BBI
from feature.zoo.BBI_Daily import BBI_Daily
from feature.zoo.BIAS10_Daily import BIAS10_Daily
from feature.zoo.BOLL import BOLL
from feature.zoo.BOLLDown_Daily import BOLLDown_Daily
from feature.zoo.BOLLUp_Daily import BOLLUp_Daily
from feature.zoo.Beta import Beta
from feature.zoo.BetaHS300_Daily import BetaHS300_Daily
from feature.zoo.CCI import CCI
from feature.zoo.CCI14_Daily import CCI14_Daily
from feature.zoo.CMO import CMO
from feature.zoo.CMO10 import CMO10
from feature.zoo.CMO20 import CMO20
from feature.zoo.CMO5 import CMO5
from feature.zoo.CVAR import CVAR
from feature.zoo.CVAR_normal_Daily import CVAR_normal_Daily
from feature.zoo.CapitalGain_Daily import CapitalGain_Daily
from feature.zoo.ChangeRate_Daily import ChangeRate_Daily
from feature.zoo.Close_Daily import Close_Daily
from feature.zoo.Close_Min_Hfq import Close_Min_Hfq
from feature.zoo.Close_Min import Close_Min
from feature.zoo.Close_Tick import Close_Tick
from feature.zoo.DEA import DEA
from feature.zoo.DEA_Daily import DEA_Daily
from feature.zoo.DIFF import DIFF
from feature.zoo.DIFF_Daily import DIFF_Daily
from feature.zoo.Elasticity import Elasticity
from feature.zoo.EMA10_Daily import EMA10_Daily
from feature.zoo.EMA10_Daily import EMA10_Daily
from feature.zoo.EMA20_Daily import EMA20_Daily
from feature.zoo.EMA30_Daily import EMA30_Daily
from feature.zoo.EMA5_Daily import EMA5_Daily
from feature.zoo.EMA60_Daily import EMA60_Daily
from feature.zoo.EMV import EMV
from feature.zoo.EMV_Daily import EMV_Daily
from feature.zoo.Financial_Period import Financial_Period
from feature.zoo.G_EPS import G_EPS
from feature.zoo.G_EPSCAGR5 import G_EPSCAGR5
from feature.zoo.G_NeToperateCashFlow import G_NeToperateCashFlow
from feature.zoo.G_NeToperateCashFlowPerShare import G_NeToperateCashFlowPerShare
from feature.zoo.G_NetAssetsPerShare import G_NetAssetsPerShare
from feature.zoo.G_NetCashFlow import G_NetCashFlow
from feature.zoo.G_NetProfit import G_NetProfit
from feature.zoo.G_NetProfit3YAvg import G_NetProfit3YAvg
from feature.zoo.G_NetProfitCAGR3 import G_NetProfitCAGR3
from feature.zoo.G_NetProfitCAGR5 import G_NetProfitCAGR5
from feature.zoo.G_OperatingProfit import G_OperatingProfit
from feature.zoo.G_OperatingRevenueCAGR3 import G_OperatingRevenueCAGR3
from feature.zoo.G_OperatingRevenueCAGR5 import G_OperatingRevenueCAGR5
from feature.zoo.G_ROE import G_ROE
from feature.zoo.G_TotalAssets import G_TotalAssets
from feature.zoo.G_TotalOperatingRevenue import G_TotalOperatingRevenue
from feature.zoo.G_TotalOperatingRevenue12QAvg import G_TotalOperatingRevenue12QAvg
from feature.zoo.G_TotalProfit import G_TotalProfit
from feature.zoo.Halflife_CVAR_Daily import Halflife_CVAR_Daily
from feature.zoo.Halflife_Kurtosis_Daily import Halflife_Kurtosis_Daily
from feature.zoo.Halflife_Momentum_Daily import Halflife_Momentum_Daily
from feature.zoo.Halflife_Std_Daily import Halflife_Std_Daily
from feature.zoo.High_Daily import High_Daily
from feature.zoo.High_Min import High_Min
from feature.zoo.Hurst import Hurst
from feature.zoo.Inv_Halflife_Std_Daily import Inv_Halflife_Std_Daily
from feature.zoo.KDJ import KDJ
from feature.zoo.KDJD_Daily import KDJD_Daily
from feature.zoo.KDJJ_Daily import KDJJ_Daily
from feature.zoo.KDJK_Daily import KDJK_Daily
from feature.zoo.Kurtosis_Daily import Kurtosis_Daily
from feature.zoo.Leo1_Daily import Leo1_Daily
from feature.zoo.Low_Daily import Low_Daily
from feature.zoo.Low_Min import Low_Min
from feature.zoo.MA10_Daily import MA10_Daily
from feature.zoo.MA20_Daily import MA20_Daily
from feature.zoo.MA30_Daily import MA30_Daily
from feature.zoo.MA5_Daily import MA5_Daily
from feature.zoo.MA60_Daily import MA60_Daily
from feature.zoo.MACD import MACD
from feature.zoo.MACD_Daily import MACD_Daily
from feature.zoo.MFI import MFI
from feature.zoo.MFI_Daily import MFI_Daily
from feature.zoo.Momentum_Daily import Momentum_Daily
from feature.zoo.Money_Daily import Money_Daily
from feature.zoo.Money_Min import Money_Min
from feature.zoo.Neu_BP import Neu_BP
from feature.zoo.Neu_CF_P import Neu_CF_P
from feature.zoo.Neu_EBIT_P import Neu_EBIT_P
from feature.zoo.Neu_EP import Neu_EP
from feature.zoo.Neu_G_EPS import Neu_G_EPS
from feature.zoo.Neu_G_EPSCAGR5 import Neu_G_EPSCAGR5
from feature.zoo.Neu_G_NeToperateCashFlow import Neu_G_NeToperateCashFlow
from feature.zoo.Neu_G_NeToperateCashFlowPerShare import Neu_G_NeToperateCashFlowPerShare
from feature.zoo.Neu_G_NetAssetsPerShare import Neu_G_NetAssetsPerShare
from feature.zoo.Neu_G_NetCashFlow import Neu_G_NetCashFlow
from feature.zoo.Neu_G_NetProfit3YAvg import Neu_G_NetProfit3YAvg
from feature.zoo.Neu_G_NetProfitCAGR3 import Neu_G_NetProfitCAGR3
from feature.zoo.Neu_G_NetProfitCAGR5 import Neu_G_NetProfitCAGR5
from feature.zoo.Neu_G_OperatingProfit import Neu_G_OperatingProfit
from feature.zoo.Neu_G_OperatingRevenueCAGR3 import Neu_G_OperatingRevenueCAGR3
from feature.zoo.Neu_G_OperatingRevenueCAGR5 import Neu_G_OperatingRevenueCAGR5
from feature.zoo.Neu_G_ROE import Neu_G_ROE
from feature.zoo.Neu_G_TotalAssets import Neu_G_TotalAssets
from feature.zoo.Neu_G_TotalOperatingRevenue import Neu_G_TotalOperatingRevenue
from feature.zoo.Neu_G_TotalOperatingRevenue12QAvg import Neu_G_TotalOperatingRevenue12QAvg
from feature.zoo.Neu_G_TotalProfit import Neu_G_TotalProfit
from feature.zoo.Neu_MV import Neu_MV
from feature.zoo.Neu_PB import Neu_PB
from feature.zoo.Neu_PCF import Neu_PCF
from feature.zoo.Neu_PE import Neu_PE
from feature.zoo.Neu_PS import Neu_PS
from feature.zoo.Neu_P_EBIT import Neu_P_EBIT
from feature.zoo.Neu_P_RE import Neu_P_RE
from feature.zoo.Neu_RE_P import Neu_RE_P
from feature.zoo.Neu_SP import Neu_SP
from feature.zoo.OBV import OBV
from feature.zoo.OBV_Daily import OBV_Daily
from feature.zoo.Open_Daily import Open_Daily
from feature.zoo.Open_Min import Open_Min
from feature.zoo.PSY import PSY
from feature.zoo.PSY_Daily import PSY_Daily
from feature.zoo.ROC import ROC
from feature.zoo.ROC_Daily import ROC_Daily
from feature.zoo.RSI import RSI
from feature.zoo.RSI6_Daily import RSI6_Daily
from feature.zoo.Rate import Rate
from feature.zoo.Rate_Daily import Rate_Daily
from feature.zoo.Return_Daily import Return_Daily,Return_NDay,Return_NDay_Label
from feature.zoo.ReferencePrice_Daily import ReferencePrice_Daily
from feature.zoo.Sharpe import Sharpe
from feature.zoo.Sharpe40_Daily import Sharpe40_Daily
from feature.zoo.Shibor_1month import Shibor_1month
from feature.zoo.Shibor_1week import Shibor_1week
from feature.zoo.Shibor_overnight import Shibor_overnight
from feature.zoo.Skewness_Daily import Skewness_Daily
from feature.zoo.Snowball_deal import Snowball_deal
from feature.zoo.Snowball_deal_week import Snowball_deal_week
from feature.zoo.Snowball_follow import Snowball_follow
from feature.zoo.Snowball_follow_week import Snowball_follow_week
from feature.zoo.Snowball_tweet import Snowball_tweet
from feature.zoo.Snowball_tweet_week import Snowball_tweet_week
from feature.zoo.Std20_Daily import Std20_Daily
from feature.zoo.TR import TR
from feature.zoo.TRIX import TRIX
from feature.zoo.TRIX_Daily import TRIX_Daily
from feature.zoo.TRMA import TRMA
from feature.zoo.TRMA_Daily import TRMA_Daily
from feature.zoo.TR_Daily import TR_Daily
from feature.zoo.TurnOver_Daily import TurnOver_Daily
from feature.zoo.TurnOver_Full_Daily import TurnOver_Full_Daily
from feature.zoo.Turnover_At_AM10 import Turnover_At_AM10
from feature.zoo.Turnover_Full_At_AM10 import Turnover_Full_At_AM10
from feature.zoo.VR import VR
from feature.zoo.VR24_Daily import VR24_Daily
from feature.zoo.Vol_Daily import Vol_Daily
from feature.zoo.Vol_Min import Vol_Min
from feature.zoo.WILLR import WILLR
from feature.zoo.WILLR_Daily import WILLR_Daily
from feature.zoo.accounts_payable import Accounts_payable
from feature.zoo.accounts_payable import Accounts_payable
from feature.zoo.accounts_receivable import Accounts_receivable
from feature.zoo.accounts_receivable_turnover_ratio import Accounts_receivable_turnover_ratio
from feature.zoo.administration_expense_cost import Administration_expense_cost
from feature.zoo.assets_liabilities_ratio import Assets_liabilities_ratio
from feature.zoo.basic_eps import Basic_eps
from feature.zoo.beginning_balance_of_cash_and_cash_equivalents import Beginning_balance_of_cash_and_cash_equivalents
from feature.zoo.bvps import Bvps
from feature.zoo.capital import Capital
from feature.zoo.capital_reserves import Capital_reserves
from feature.zoo.cash_inflow_from_financing_activities import Cash_inflow_from_financing_activities
from feature.zoo.cash_inflow_from_investment_activities import Cash_inflow_from_investment_activities
from feature.zoo.cash_inflows_from_operating_activities import Cash_inflows_from_operating_activities
from feature.zoo.cash_outflow_for_financing_activities import Cash_outflow_for_financing_activities
from feature.zoo.cash_outflow_for_investment_activities import Cash_outflow_for_investment_activities
from feature.zoo.cash_outflow_for_operating_activities import Cash_outflow_for_operating_activities
from feature.zoo.cash_ratio import Cash_ratio
from feature.zoo.cost_of_sales import Cost_of_sales
from feature.zoo.current_ratio import Current_ratio
from feature.zoo.deferred_income_tax_assets import Deferred_income_tax_assets
from feature.zoo.diluted_eps import Diluted_eps
from feature.zoo.eps import Eps
from feature.zoo.equity import Equity
from feature.zoo.equity_to_debt_ratio import Equity_to_debt_ratio
from feature.zoo.final_balance_of_cash_and_cash_equivalents import Final_balance_of_cash_and_cash_equivalents
from feature.zoo.financial_expenses import Financial_expenses
from feature.zoo.fixed_assets import Fixed_assets
from feature.zoo.gpr import Gpr
from feature.zoo.gross_margin import Gross_margin
from feature.zoo.increasing_rate_of_eps import Increasing_rate_of_eps
from feature.zoo.intangible_assets import Intangible_assets
from feature.zoo.interest_coverage_ratio import Interest_coverage_ratio
from feature.zoo.inventory import Inventory
from feature.zoo.inventory_turnover_ratio import Inventory_turnover_ratio
from feature.zoo.lev import Lev
from feature.zoo.moig import Moig
from feature.zoo.nav import Nav
from feature.zoo.net_asset_turnover_ratio import Net_asset_turnover_ratio
from feature.zoo.net_cash_flow_for_investment_activities import Net_cash_flow_for_investment_activities
from feature.zoo.net_cash_flow_for_operating_activities import Net_cash_flow_for_operating_activities
from feature.zoo.net_cash_flow_from_financing_activities import Net_cash_flow_from_financing_activities
from feature.zoo.net_margin import Net_margin
from feature.zoo.net_profit import Net_Profit
from feature.zoo.net_profit_growth_rate import Net_profit_growth_rate
from feature.zoo.nonbusiness_expenditure import Nonbusiness_expenditure
from feature.zoo.nonbusiness_income import Nonbusiness_income
from feature.zoo.npr import Npr
from feature.zoo.ocfps import Ocfps
from feature.zoo.operating_expenses import Operating_expenses
from feature.zoo.operating_margin import Operating_margin
from feature.zoo.operating_profit import Operating_profit
from feature.zoo.operating_profit import Operating_profit
from feature.zoo.orps import Orps
from feature.zoo.paid_in_capital import Paid_in_capital
from feature.zoo.quick_ratio import Quick_ratio
from feature.zoo.Recovery_Factor import Recovery_Factor
from feature.zoo.revenue import Revenue
from feature.zoo.right_coefficient import Right_coefficient
from feature.zoo.rnavps import Rnavps
from feature.zoo.roa import Roa
from feature.zoo.roe import Roe
from feature.zoo.roi import Roi
from feature.zoo.subsidize_revenue import Subsidize_revenue
from feature.zoo.total_assets import Total_assets
from feature.zoo.total_assets import Total_assets
from feature.zoo.total_assets_turnover_ratio import Total_assets_turnover_ratio
from feature.zoo.total_current_assets import Total_current_assets
from feature.zoo.total_current_liability import Total_current_liability
from feature.zoo.total_liabilities import Total_liabilities
from feature.zoo.total_noncurrent_assets import Total_noncurrent_assets
from feature.zoo.total_noncurrent_liabilities import Total_noncurrent_liabilities
from feature.zoo.total_owners_equity import Total_owners_equity
from feature.zoo.total_profit import Total_profit
from feature.zoo.total_profit import Total_profit


from feature.zoo.Total_Shares import Total_Shares
from feature.zoo.Onmarket_Time import Onmarket_Time


from feature.zoo.Price_Tick import Ask_Price_Tick1,Ask_Price_Tick2,Ask_Price_Tick3,Ask_Price_Tick4,Ask_Price_Tick5,Bid_Price_Tick1,Bid_Price_Tick2,Bid_Price_Tick3,Bid_Price_Tick4,Bid_Price_Tick5
from feature.zoo.Vol_Tick import Ask_Vol_Tick1,Ask_Vol_Tick2,Ask_Vol_Tick3,Ask_Vol_Tick4,Ask_Vol_Tick5,Bid_Vol_Tick1,Bid_Vol_Tick2,Bid_Vol_Tick3,Bid_Vol_Tick4,Bid_Vol_Tick5,Vol_Tick
from feature.zoo.TickAbsentTag import Tick_Absent
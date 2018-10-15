#输入预期订单
class Order:

     #输入交易代码，交易日期，交易时间，交易类型，买或者卖（卖是全部卖出），购买比例(如果是零默认均分，最终购买手数会转化为amounts变量)，如果是限价单需要给出价格，限价单的有效期(默认为零)
    def __init__(self,code,date,time,type='M',buySell='b',buy_portion=0,l_pice=0.0,valid_duration=0):
        self.code=code #股票代码
        self.date=date #'2017061203'
        self.time=time #'110808'
        self.order_date=date #'2017061203'
        self.order_time=time #'110808'
        self.type=type #交易类别 M市价单 L为限价单 默认为M市价单
        self.buy_sell=buySell #b代表买 s代表卖
        self.amounts=0 #购买或者卖出手数
        self.buy_portion=buy_portion # 购买占总金额的比例
        self.trade_capital = 0  # 购买占总金额的比例
        self.l_price=float(l_pice) #限价单价格
        self.valid_duration=int(valid_duration)

    '''def computeBuyAmount(self,totalCaptial):
        if self.buySell=='b':
            self.tradeCapital=(int)(float(totalCaptial) * float(self.buyPortion))'''


        #self.validDuration=validDuration #订单有效时长
        #self.price=price #委托价格





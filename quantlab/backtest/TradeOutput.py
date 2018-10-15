
#回测交易订单
class TradeOutput:

    #手续费买入卖出都需要交
    #印花税仅卖出需要交
    #默认两者为0
    #输入为 当前订单，真实交易时间，真实平均股票交易价格，真实交易数量，手续费，印花税仅当卖出时有效
    def __init__(self, order, real_time, real_stock_price, real_amounts, earnorloss,poundage, stamp_cost=0):
        self.code = order.code  # 股票代码
        self.date = order.date  # '2017061203'
        self.time = order.time  # '110808' 小时分钟秒
        self.order_date=order.order_date
        self.order_time=order.order_time
        self.type = order.type  # 交易类别 M市价单 L为限价单 默认为M市价单
        self.buy_sell = order.buy_sell  # b代表买 s代表卖
        self.amounts = int(order.amounts)  # 购买或者卖出手数

        self.buy_portion = order.buy_portion  # 购买占总金额的比例
        self.limit_price = float(order.l_price)
        self.valid_duration = int(order.valid_duration)


        self.real_time=real_time #具体交易的时间（最后一个tick的参考时间）
        self.real_stock_price=real_stock_price #实际股票价格（平均价格）
        self.real_amounts=real_amounts #实际交易数量(以手为单位)
        self.poundage_cost=poundage #手续费
        if self.buy_sell== 's':
            self.stamp_cost=stamp_cost#印花税
        else:
            self.stamp_cost=0
        self.stock_return = earnorloss
        # print(order.code + " " + order.time + " " + str(self.real_stock_price) + " " + str( self.real_amounts) + " " + str(self.poundage_cost + self.stamp_cost))

        #print ("trade "+order.code+" amount： "+str(self.actualAmounts)+" price "+ str(self.actualStockPrice)+" total :"+ str(self.actualAmounts*100*self.actualStockPrice+self.poundageCost+self.stampCost))

    def tostring(self,):
        return "code= " + self.code + " orderdate= " + self.date + " ordertime= " + self.time +" actualTime= " + self.real_time + " actualStockPrice= " + str(
            self.real_stock_price) + " actualAmounts= " + str(self.real_amounts) + \
               " poundageCost= " + str(self.poundage_cost) + " stampCost= " + str(self.stamp_cost)
'''return "code= "+self.code+" orderdate= "+self.date+" ordertime= "+self.time + " type= " + self.type + " buySell= " + self.buy_sell + " amounts= " + str(self.amounts) + " buyPortion= " + str(self.buy_portion) + " limitPrice= " + str(self.limit_price) +\
               " validDuration= "+str(self.valid_duration) + " actualTime= " + self.real_time + " actualStockPrice= " + str(self.real_stock_price) + " actualAmounts= " + str(self.real_amounts) +\
               " poundageCost= "+str(self.poundage_cost) + " stampCost= " + str(self.stamp_cost)'''



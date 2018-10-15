class Minute:
    def __init__(self,time,price,count,flag_buy,flag_sell):
        #self.code=code #股票代码
        self.time=str(time) #几分钟几秒
        self.price=float(price)#成交价格
        self.count=float(count) #成交手数
        self.up_stop_point = float(flag_buy)  # 涨停点
        self.down_stop_point = float(flag_sell)  # 跌停点
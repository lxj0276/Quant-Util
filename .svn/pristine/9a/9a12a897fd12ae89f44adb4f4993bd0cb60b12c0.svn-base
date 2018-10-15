
class Stock:
    def __init__(self,code,amounts,price,date):
        self.code=code
        self.amounts=int(amounts)
        self.average_price=float(price)
        self.last_ratio=0
        self.buy_date=date
        self.pundage_cost=0 #购买时的手续费
        self.close_assets=-1
        
    def update(self,amouts,price):
        #print (str(self.amounts)+" "+str(amouts))
        #print ("average price"+str(self.average_price)+" "+str(self.amounts)+" "+str(amouts))
        self.average_price= (self.average_price * self.amounts + amouts * price) / (self.amounts + amouts)
        self.amounts+=amouts

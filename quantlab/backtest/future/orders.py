# -*- coding: utf-8 -*-

class MarketOrder(object):

    def __init__(self, amount, create_time):
        self.amount_total = amount
        self.create_time  = create_time
        self.update_time  = create_time
        self.amount_traded = 0.0

    @property
    def amount(self):
        return self.amount_total - self.amount_traded

from quantlab.feature.ops import *

def ROC(close, window=12):
    close_before = Shift(close, window)
    return Map(Div(close, close_before), lambda x:(x-1)*100)
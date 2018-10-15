from quantlab.feature.ops import *

def BIAS(close, window=10):
    return Div(Sub(close, MA(close,window)), MA(close,window))
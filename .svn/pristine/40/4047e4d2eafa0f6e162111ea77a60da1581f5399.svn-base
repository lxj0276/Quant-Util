from quantlab.feature.ops import *


def TR1(close, high, low):
	temp = Sub(Shift(close, 1), low)
	TR1 = Multi_rolling([temp, np.zeros(len(temp))], 1, lambda x:x.squeeze().max())
	return TR1
from numpy.core.umath import exp, sqrt, pi
from scipy.integrate import quad

from feature.ops import *


def CVAR(change, window=40, n=2):
    '''
    CVAR 计算前window天（包括今天）收益率的均值和方差
    并认为收益率分布符合正态分布，在负无穷到mu-2sigma范围内
    对收益率按正态分布积分。表示极端情况下亏损情况，通常情况下是负值，
    越小风险越大
    '''

    def get_CVAR(x):
        mu = nanmean(x)
        sig = nanstd(x)
        return calculate_normfit_cum_expect(mu - n * sig, mu, sig)

    def calculate_normfit_pdf(x, mu, sig):
        return exp(-(x - mu) ** 2 / (2 * sig ** 2)) / (sqrt(2 * pi) * sig)

    def calculate_normfit_cum_expect(x, mu, sig):
        return quad(lambda x: x * calculate_normfit_pdf(x, mu, sig), mu - 10 * sig, x)[0]

    return Rolling(change, window, get_CVAR)

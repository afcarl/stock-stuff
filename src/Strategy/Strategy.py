from src.Indicators.AccumulationDistribution import AccumulationDistribution
from src.Indicators.BollingerBand import BollingerBand
from src.Indicators.CCI import CCI
from src.Indicators.ChaikinOscillator import ChaikinOscillator
from src.Indicators.MACD import MACD
from src.Indicators.MovingAverage import MovingAverage
from src.Indicators.OBV import OnBalanceVolume
from src.Indicators.RSI import RSI
from src.Indicators.Stochastic import Stochastic
from src.Indicators.SupportResistance import SupportResistance
from src.Indicators.WilliamsR import WilliamsR

'''
A strategy is a class that takes in a data point, then signals a buy, sell, or hold
Ideally, for bear plays, it would just reverse buy and sell

in the future, it will signal buy at, take profit at, and stop loss at

'''

class Strategy:

    def __init__(self):
        self.index = 0
        self.data_points = []
        self.indicators = []
        self.indicators.append(AccumulationDistribution(self.data_points))
        self.indicators.append(BollingerBand(self.data_points,20))
        self.indicators.append(CCI(self.data_points,20))
        self.indicators.append(ChaikinOscillator(self.data_points,3,10))
        self.indicators.append(MACD(self.data_points,12,26,9))
        self.indicators.append(MovingAverage(self.data_points,20))
        self.indicators.append(OnBalanceVolume(self.data_points))
        self.indicators.append(RSI(self.data_points,14))
        self.indicators.append(Stochastic(self.data_points,14))
        self.indicators.append(SupportResistance(self.data_points,100))
        self.indicators.append(WilliamsR(self.data_points,14))

    def tick(self, data_point):
        self.data_points.append(data_point)
        for indicator in self.indicators:
            indicator.calculate_point(self.index)
        self.index += 1
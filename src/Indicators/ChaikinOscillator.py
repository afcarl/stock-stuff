from src.Indicators import *
from src.Indicators.MovingAverage import MovingAverage
from src.Indicators.AccumulationDistribution import AccumulationDistribution

class ChaikinOscillator(Indicator):

    def __init__(self, data_points, period1, period2):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.ma_1 = MovingAverage([],period1, period1)
        self.ma_2 = MovingAverage([],period2, period2)
        self.ADL = AccumulationDistribution(data_points)

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    def calculate_point(self, index):
        ad = self.ADL.calculate_point(index)
        self.ma_1.enqueue(ad)
        self.ma_2.enqueue(ad)
        return self.ma_1.calculate_point(index) - self.ma_2.calculate_point(index)

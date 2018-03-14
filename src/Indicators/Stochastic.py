from src.Indicators import *
from src.Indicators.MovingAverage import MovingAverage
class Stochastic(Indicator):

    def __init__(self, data_points, period):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period
        self.d_ma = MovingAverage([],3,3)

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    def calculate_point(self, index):
        points = self.data_points[-self.period:]
        close = self.data_points[index].close
        closes = [p.close for p in points]
        lowest = min(closes)
        highest = max(closes)

        k = 100.0 *(close - lowest) / (highest - lowest)
        self.d_ma.enqueue(k)
        d = self.d_ma.calculate_point(index)

        return k,d

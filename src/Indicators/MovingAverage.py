from src.Indicators import *

class MovingAverage(Indicator):

    def __init__(self, data_points, period):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i+1)

    def calculate_point(self, index):
        low = index-self.period if index - self.period > 0 else 0
        points = self.data_points[low: index]
        period = len(points)
        closes = [p.close for p in points]
        return sum(closes) / float(period)

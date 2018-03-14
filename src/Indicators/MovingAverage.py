from src.Indicators import *
from src.DataPoint import DataPoint

class MovingAverage(Indicator):

    def __init__(self, data_points, period, max_size=None):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period
        self.max_size=max_size

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    def calculate_point(self, index):
        # max size will be none if data_points come straight from historical stock data
        if self.max_size is None:
            points = self.data_points[-self.period:]
        else:
            #max size will be set if this MA is of an indicator, like the signal line for MACD
            points = self.data_points

        period = len(points)
        if isinstance(points[0], DataPoint):
            closes = [p.close for p in points]
        else:
            closes = points
        return sum(closes) / float(period)

    def enqueue(self, data_point):
        self.data_points.insert(0,data_point)
        if self.max_size is not None:
            if len(self.data_points) > self.max_size:
                self.dequeue()

    def dequeue(self):
        return self.data_points.pop()


from src.Indicators import *


class WilliamsR(Indicator):

    def __init__(self, data_points, period):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    def calculate_point(self, index):
        dp = self.data_points[index]
        highest = max([dp.close for dp in self.data_points[-self.period:]])
        lowest = min([dp.close for dp in self.data_points[-self.period:]])

        r = (highest - dp.close) / (highest - lowest) * -100.0
        return r
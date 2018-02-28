from src.Indicators import *

class AccumulationDistribution(Indicator):

    def __init__(self, data_points):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.ADL = 1.0

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i+1)

    def calculate_point(self, index):
        dp = self.data_points[index]
        money_flow_multiplier = ((dp.close - dp.low) - (dp.high - dp.close)) / (dp.high - dp.low)

        money_flow_volume = money_flow_multiplier * dp.volume
        self.ADL += money_flow_volume
        return self.ADL
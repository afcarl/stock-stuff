from src.Indicators import *
from src.Indicators.MovingAverage import MovingAverage

class CCI(Indicator):

    def __init__(self, data_points, period):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period
        self.tp_ma = MovingAverage([],period,period)

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i+1)

    def calculate_point(self, index):
        dp = self.data_points[index]
        typical = (dp.high + dp.low + dp.close) / 3.0
        self.tp_ma.enqueue(typical)
        latest_tp_ma = self.tp_ma.calculate_point(index)
        diffs = [latest_tp_ma - tp for tp in self.tp_ma.data_points]
        diffs = [abs(diff) for diff in diffs]
        mean_deviation = sum(diffs) / float(self.period)

        cci = (typical - latest_tp_ma) / (.015*mean_deviation)
        return cci
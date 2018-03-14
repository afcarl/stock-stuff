from src.Indicators import *
from src.Indicators.MovingAverage import MovingAverage
from src.DataPoint import DataPoint

class MACD(Indicator):

    def __init__(self, data_points, ma1_period=12, ma2_period=26, signal_period=9):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.ma1_period = ma1_period
        self.ma2_period = ma2_period
        self.signal_period = signal_period

        self.ma1 = MovingAverage(data_points,ma1_period)
        self.ma2 = MovingAverage(data_points,ma2_period)

        self.signal = MovingAverage([], signal_period, max_size=signal_period)

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    def calculate_point(self, index):
        m1 = self.ma1.calculate_point(index)
        m2 = self.ma2.calculate_point(index)

        macd = m1 - m2
        self.signal.enqueue(macd)
        sig = self.signal.calculate_point(index)
        return m1 - m2, sig



from src.Indicators import *
from src.Indicators.MovingAverage import MovingAverage


class MACD(Indicator):

    def __init__(self, data_points, ma1_period=12, ma2_period=26, signal_period=9):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.ma1_period = ma1_period
        self.ma2_period = ma2_period
        self.signal_period = signal_period

        self.ma1 = MovingAverage(data_points,ma1_period)
        self.ma2 = MovingAverage(data_points,ma2_period)

        self.macds = list()

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i+1)

    def calculate_point(self, index):
        m1 = self.ma1.calculate_point(index)
        m2 = self.ma2.calculate_point(index)

        macd = m1 - m2
        self.macds.insert(0,macd)
        if len(self.macds) > self.signal_period:
            self.macds.pop()
        sig = sum(self.macds) / float(self.signal_period)
        print('ma1',m1)
        print('ma2',m2)
        return m1 - m2, sig



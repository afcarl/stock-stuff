from src.Indicators import *
from src.Utils.FileHandling.CSV.csv_file import CSVFile
import matplotlib.pyplot as plt


class RSI(Indicator):

    def __init__(self, data_points, period):
        self.data_points = data_points
        self.period = period
        self.avg_gain = 0.0
        self.avg_loss = 0.0

    def calculate_point(self, index):
        dp = self.data_points[index]
        prev_dp = self.data_points[index - 1]
        diff = dp.close - prev_dp.close
        if diff > 0:
            gain = diff
            loss = 0.0
        else:
            gain = 0.0
            loss = abs(diff)
        self.avg_gain = (self.avg_gain * (self.period-1) + gain) / float(self.period)
        self.avg_loss = (self.avg_loss * (self.period-1) + loss) / float(self.period)
        RS = self.avg_gain / self.avg_loss
        yield dp.minutes, 100.0 - (100.0 / (1.0 + RS))


    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

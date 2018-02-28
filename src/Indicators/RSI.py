from src.Indicators import *
from src.Utils.FileHandling.CSV.csv_file import CSVFile
import matplotlib.pyplot as plt


class RSI(Indicator):

    def __init__(self, data_points, period):
        self.data_points = data_points
        self.period = period

    def calculate(self):
        avg_gain = avg_loss = 1.0
        prev_dp = self.data_points[0]
        for i,dp in enumerate(self.data_points[1:]):
            diff = dp.close - prev_dp.close
            if diff > 0:
                gain = diff
                loss = 0.0
            else:
                gain = 0.0
                loss = abs(diff)
            prev_dp = dp
            avg_gain = (avg_gain * (self.period-1) + gain) / float(self.period)
            avg_loss = (avg_loss * (self.period-1) + loss) / float(self.period)
            RS = avg_gain / avg_loss
            yield dp.minutes, 100.0 - (100.0 / (1.0 + RS))

    def score(self, rsi):
        # rsi is scaled from 0 - 100 on buy -> sell
        #so subtract 50, then multiple by -2 to scale and reverse to sell -> buy -100 -> +100
        return (rsi - 50.0) * -2.0

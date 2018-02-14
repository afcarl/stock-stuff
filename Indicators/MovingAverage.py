import matplotlib.pyplot as plt

from Indicators import *
from Utils.FileHandling.CSV.csv_file import CSVFile

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

with CSVFile('../data/daily/table_qcom.csv', 'rt') as f:
    data_points = list(f.read_datapoints())
    ma = MovingAverage(data_points, 20)
    x_axis = []
    y_axis = []
    for minutes, point in ma.calculate():
        x_axis.append(minutes)
        y_axis.append(point)
    plt.plot(x_axis, y_axis)
    plt.show()
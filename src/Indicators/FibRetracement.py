from src.Indicators import *
from src.Analysis.LocalMinMax import find_local_maxima,find_local_minima

class FibRetracement(Indicator):

    #period probably isn't the right word, but it's the amount of periods to look back
    def __init__(self, data_points, period=100):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)


    #returns 23.6, 38, 50, 62 percent retracements between the mean and max from the previous 100 points
    def calculate_point(self, index):
        dp = self.data_points[index]
        pass
from src.Indicators import *
from src.Analysis.LocalMinMax import find_local_maxima,find_local_minima

class SupportResistance(Indicator):

    #period probably isn't the right word, but it's the amount of periods to look back
    def __init__(self, data_points, period=100):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    #returns [supports],[resistances] within period of index.
    def calculate_point(self, index):
        dp = self.data_points[index]

        maxima = find_local_maxima(self.data_points[-self.period:],5)
        minima = find_local_minima(self.data_points[-self.period:],5)

        supports = [m for m in minima if m < dp.close]
        resistances = [m for m in maxima if m > dp.close]

        return supports,resistances
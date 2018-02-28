from src.Indicators import *
from src.DataPoint import DataPoint

class Stochastic(Indicator):

    def __init__(self, data_points, period):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.period = period
        self.prev_d = list()

    def calculate(self):
        prev_dp = DataPoint.default_data_point()
        prev_sar = 0.0
        for i, dp in enumerate(self.data_points):
            pass


    def calculate_point(self, index):
        pass
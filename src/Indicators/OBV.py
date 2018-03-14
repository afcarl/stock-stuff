from src.Indicators import *

class OnBalanceVolume(Indicator):

    def __init__(self, data_points):
        assert isinstance(data_points, list), "moving average must take a list, not an iterator"
        self.data_points = data_points
        self.OBV = 0

    def calculate(self):
        for i, dp in enumerate(self.data_points):
            yield dp.minutes, self.calculate_point(i)

    def calculate_point(self, index):
        prev_dp = self.data_points[index-1]
        dp = self.data_points[index]

        #if the close price (to the cent, anyway) is the same we don't do anything
        if abs(dp.close - prev_dp.close) < .01:
            pass
        elif dp.close > prev_dp.close:
            self.OBV += dp.volume
        elif dp.close < prev_dp.close:
            self.OBV -= dp.volume
        else:
            #unreachable?
            pass

        return self.OBV
    
from enum import Enum

import os
from src.Utils.FileHandling import DataFile


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Timespan(Enum):
    MINUTES_1  = 1
    MINUTES_5  = 5
    MINUTES_15 = 15
    MINUTES_30 = 30
    HOURS_1    = 60
    HOURS_2    = 120
    HOURS_4    = 240
    DAY_1      = 390
    WEEK_1     = 1950
    MONTH_1    = 7800

class StockDataProvisioner:

    def __init__(self, stock, timespan,):
        self.stock = stock
        self.timespan = timespan

        if self.timespan.value < 390:
            if self.timespan.value not in [1,5,15,30,60,12,240]:
                raise ValueError('Invalid value for data timespan')
            folder = str(self.timespan.value) + 'minute'
        elif self.timespan == Timespan.DAY_1:
            folder = '1day'
        elif self.timespan == Timespan.WEEK_1:
            folder = '1week'
        elif self.timespan == Timespan.MONTH_1:
            folder = '1month'
        else:
            raise ValueError('Invalid value for data timespan')
        path = os.path.join(ROOT_DIR, 'data', folder, self.stock.upper()) + '.hid.gz'

        self.underlying = DataFile(path,'r')

    def read_datapoints(self, start=None, stop=None):
        yield from self.underlying.read_datapoints()

    def __enter__(self):
        return self.underlying.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.underlying.__exit__(exc_type,exc_val,exc_tb)
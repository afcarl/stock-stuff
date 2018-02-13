from collections import namedtuple
import datetime
import os
import time
import struct

from enum import Enum


def default_data_point():
    return DataPoint(datetime.datetime.strptime('19690101', '%Y%m%d').date(),
                     datetime.timedelta(seconds=0),
                     1.0,
                     1.0,
                     1.0,
                     1.0,
                     1.0,)

def find_data(data_points):
    minutes = data_points[0].minutes
    high = 0.0
    low = 9999999999999.0
    volume = 0
    open_ = data_points[0].open
    close = data_points[-1].close
    for dp in data_points:
        if dp.high > high:
            high = dp.high
        if dp.low < low:
            low = dp.low
        volume += dp.volume
    return DataPoint(0, 0, open_, high, low, close, volume, minutes)

def gen_new_intraday(data_points, num_minutes):
    ret = []
    all_periods = zip(*[iter(data_points)]*num_minutes)
    for chunk in all_periods:
        ret.append(find_data(chunk))
    return ret


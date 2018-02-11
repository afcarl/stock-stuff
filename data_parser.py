from collections import namedtuple
import datetime
import os
import time

class DataPoint:
    __slots__ = ['minutes', 'open', 'high', 'low', 'close', 'volume']
    def __init__(self, date, timestamp, open_, high, low, close, volume):

        self.minutes = int((time.mktime(date.timetuple()) + timestamp.total_seconds()) / 60)
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume= volume



def default_data_point():
    return DataPoint(datetime.datetime.strptime('19690101', '%Y%m%d').date(),
                     datetime.timedelta(seconds=0),
                     1.0,
                     1.0,
                     1.0,
                     1.0,
                     1.0,)

def line_to_data_point(line):
    args = []
    data_points = line.split(',')
    try:
        args.append(datetime.datetime.strptime(data_points[0], '%Y%m%d').date())
    except:
        args.append(datetime.datetime.strptime(data_points[0], '%m/%d/%Y').date())

    t = data_points[1]
    if len(t) == 1:
        td = datetime.timedelta(seconds=0)
    elif len(t) == 4:
        td = datetime.timedelta(hours=int(t[0:2]), minutes=int(t[2:4]))
    elif len(t) == 5:
        td = datetime.timedelta(hours=int(t[0:2]), minutes=int(t[3:5]))
    args.append(td)

    args.append(float(data_points[2])) #open
    args.append(float(data_points[3])) #high
    args.append(float(data_points[4])) #low
    args.append(float(data_points[5])) #close
    args.append(float(data_points[6])) #volume

    return DataPoint(*args)


def parse_csv(path):
    if path.endswith('.xz'):
        import lzma
        open = lzma.open
    else:
        import builtins
        open = builtins.open
    with open(path,'rt') as f:
        for line in f:
            line = line.strip()
            dp = line_to_data_point(line)
            yield dp

import pprint

import time
start = time.time()
#data = list(parse_csv('data/daily/table_qcom.csv'))
#data = list(parse_csv('data/minute/ibm.csv'))
#end = time.time()
#print('took {} ms to parse xz'.format((end-start)*1000))

pprint.pprint(list(parse_csv('data/daily/table_qcom.csv.xz')))
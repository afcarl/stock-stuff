import time
import datetime
import struct
import numpy
from src.Utils.FileHandling.HID import HIDType

def date_timestamp_to_seconds(date, timestamp):
    return int((time.mktime(date.timetuple()) + timestamp.total_seconds()))

def date_timestamp_to_minutes(date, timestamp):
    return date_timestamp_to_seconds(date,timestamp) / 60

class DataPoint:
    __slots__ = ['minutes', 'open', 'high', 'low', 'close', 'volume']

    def __init__(self, open_=None, high=None, low=None, close=None, volume=None, minutes=None, date=None, timestamp=None, packed=None, csv_line=None, hid_type=None):

        if packed:
            self.unpack(packed, hid_type)
        elif csv_line:
            self.from_csv_line(csv_line)
        else:
            if minutes is None:
                self.minutes = date_timestamp_to_minutes(date,timestamp)
            else:
                self.minutes = minutes
            self.open = open_
            self.high = high
            self.low = low
            self.close = close
            self.volume = volume

    def to_csv_line(self):
        args = [str(self.minutes), str(self.open), str(self.high), str(self.low), str(self.close), str(self.volume)]
        return ','.join(args)

    def from_csv_line(self, line):
        data_points = str(line).split(',')
        if len(data_points) == 6:
            # time and date have been combined to the first field to mean "minutes since epoch"
            self.minutes = int(data_points.pop(0))
        elif len(data_points) == 7:
            date = data_points.pop(0)
            try:
                date = datetime.datetime.strptime(date, '%Y%m%d').date()
            except:
                date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

            t = data_points.pop(0)
            if len(t) == 4:
                td = datetime.timedelta(hours=int(t[0:2]), minutes=int(t[2:4]))
            elif len(t) == 5:
                td = datetime.timedelta(hours=int(t[0:2]), minutes=int(t[3:5]))
            else:
                td = datetime.timedelta(seconds=0)
            self.minutes = int((time.mktime(date.timetuple()) + td.total_seconds()) / 60)

        self.open = float(data_points.pop(0))
        self.high = float(data_points.pop(0))
        self.low = float(data_points.pop(0))
        self.close = float(data_points.pop(0))
        self.volume = int(float(data_points.pop(0)))

    def pack(self, hid_type):
        format_str = HIDType.get_entry_format_str(hid_type)
        return struct.pack(format_str,self.minutes, self.volume, self.open, self.high, self.low, self.close)

    def unpack(self, packed, hid_type):
        format_str = HIDType.get_entry_format_str(hid_type)
        self.minutes, self.volume, self.open, self.high, self.low, self.close = struct.unpack(format_str, packed)

    def __str__(self):
        return "minutes: {} open: {:.3f} high: {:.3f} low: {:.3f} close: {:.3f} volume:{}".format(self.minutes,self.open,self.high,self.low,self.close,self.volume)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def default_data_point(self):
        return DataPoint(datetime.datetime.strptime('19690101', '%Y%m%d').date(),
                         datetime.timedelta(seconds=0),
                         1.0,
                         1.0,
                         1.0,
                         1.0,
                         1.0, )

    @staticmethod
    def interpolate_datapoint(dp1, dp2):
        minutes = range(dp1.minutes+1, dp2.minutes)
        opens = numpy.interp(minutes,[dp1.minutes,dp2.minutes], [dp1.open,dp2.open])
        highs = numpy.interp(minutes,[dp1.minutes,dp2.minutes], [dp1.high,dp2.high])
        lows = numpy.interp(minutes,[dp1.minutes,dp2.minutes], [dp1.low,dp2.low])
        closes = numpy.interp(minutes,[dp1.minutes,dp2.minutes], [dp1.close,dp2.close])
        volumes = numpy.interp(minutes,[dp1.minutes,dp2.minutes], [dp1.volume,dp2.volume])
        volumes = list(map(int,volumes))
        ret = []
        for i in range(0,len(minutes)):
            dp =DataPoint(minutes=minutes[i],open_=opens[i],high=highs[i],low=lows[i],close=closes[i],volume=volumes[i])
            ret.append(dp)

        return ret
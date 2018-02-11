import datetime
import lzma
from data_parser import DataPoint

def line_to_data_point(line):
    kwargs = dict()
    data_points = str(line).split(',')
    if len(data_points) == 6:
        # time and date have been combined to the first field to mean "minutes since epoch"
        kwargs['minutes'] = int(data_points.pop(0))
    elif len(data_points) == 7:
        date = data_points.pop(0)
        try:
            kwargs['date'] = datetime.datetime.strptime(date, '%Y%m%d').date()
        except:
            kwargs['date'] = datetime.datetime.strptime(date, '%m/%d/%Y').date()

        t = data_points.pop(0)
        if len(t) == 4:
            td = datetime.timedelta(hours=int(t[0:2]), minutes=int(t[2:4]))
        if len(t) == 5:
            td = datetime.timedelta(hours=int(t[0:2]), minutes=int(t[3:5]))
        else:
            td = datetime.timedelta(seconds=0)
        kwargs['timestamp'] = td

    kwargs['open_'] = float(data_points.pop(0))
    kwargs['high'] = float(data_points.pop(0))
    kwargs['low'] = float(data_points.pop(0))
    kwargs['close'] = float(data_points.pop(0))
    kwargs['volume'] = int(float(data_points.pop(0)))

    return DataPoint(**kwargs)

class CSVFile:

    def __init__(self, path, permissions='rt'):
        self.path = path
        self.permissions = permissions
        self.fp = None

    def __enter__(self):
        if self.path.endswith('.xz'):
            import lzma
            open = lzma.open
        elif self.path.endswith('.gz'):
            import gzip
            open = gzip.open
        else:
            import builtins
            open = builtins.open
        self.fp = open(self.path, self.permissions)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

    def read_datapoints(self):
        for line in self.fp:
            print(line)
            line = line.strip()
            dp = line_to_data_point(line)
            yield dp

    def write_datapoints(self, data_points):
        #there's a very real possibility that we're reading from and writing to the same file
        #so we need to copy the entire data_points and then seek back to the beginning
        data_points = list(data_points)
        self.fp.seek(0)
        for dp in data_points:
            self.fp.write(dp.to_csv_line() + '\n')

with CSVFile('data/daily/table_qcom.csv','rt') as f:
    data = list(f.read_datapoints())

with CSVFile('data/daily/table_qcom.csv', 'w') as f:
    f.write_datapoints(data)
import datetime
import lzma
from data_parser import DataPoint

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
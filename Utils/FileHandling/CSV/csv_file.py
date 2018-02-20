
from DataPoint import DataPoint

class CSVFile:

    def __init__(self, path, permissions='rt+', *args, **kwargs):
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

        try:
            line = self.fp.readline()
            if not line.startswith('"Date"'):
                self.fp.seek(0)
        except:
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

    def read_datapoints(self):
        while True:
            lines = self.fp.readlines(65536)
            if not lines:
                break
            for line in lines:
                yield DataPoint(csv_line=line)

    def write_datapoints(self, data_points):
        self.fp.seek(0)
        out_str = ''
        for dp in data_points:
            out_str += dp.to_csv_line() + '\n'
            if len(out_str) >= 65536:
                self.fp.write(out_str)
                out_str = ''
        self.fp.write(out_str)

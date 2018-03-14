
from src.DataPoint import DataPoint
from src.Utils import chunks
#43 is the ascii code for '+', and all of our other valid umcsv nibbles are the values immediately following this
#so we can just add 43 to the nobble to get the ascii code
def expand_buf(buf):
    ret = ''
    for b in buf:
        h = (int(b.hex(),16) >> 4) & 0xf
        l = int(b.hex(),16) & 0xf
        ret += (chr(h+43))
        ret += (chr(l+43))
    return ret

def compress_buf(buf):
    ret = b''
    for b in buf:


class UMCSVFile:

    def __init__(self, path, permissions='rb+', *args, **kwargs):
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
            #TODO: figure out how to embed the csv header thing
            pass
        except:
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()



    def read_datapoints(self):
        buf = self.fp.read()
        header, buf = buf.split('\n',1)
        expanded = expand_buf(buf)
        buf = None #lets go ahead and None this and maybe the garbage collector will run if necessary
        for raw_data in chunks(buf.split(','),len(header.split(','))):
            print(raw_data)

    def write_datapoints(self, data_points):
        self.fp.seek(0)
        out_str = ''
        for dp in data_points:
            out_str += dp.to_csv_line() + '\n'
            if len(out_str) >= 65536:
                self.fp.write(out_str)
                out_str = ''
        self.fp.write(out_str)

import os
from src.Utils.FileHandling.CSV.csv_file import CSVFile
from src.Utils.FileHandling.HID.hid_file import HIDFile


class DataFile:
    def __init__(self, path, permissions, *args, **kwargs):
        file_type = ''
        path_parts = os.path.basename(path).split('.')
        index = -1
        if path_parts[index] in ['gz','xz']:
            index = -2
        if path_parts[index] == 'csv':
            if 't' not in permissions:
                permissions += 't'
            self.underlying = CSVFile(path, permissions, *args, **kwargs)
        elif path_parts[index] == 'hid':
            if 'b' not in permissions:
                permissions += 'b'
            self.underlying = HIDFile(path, permissions, *args, **kwargs)

    def __enter__(self):
        return self.underlying.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.underlying.__exit__(exc_type,exc_val,exc_tb)

    def write_datapoints(self, *args, **kwargs):
        self.underlying.write_datapoints(*args, **kwargs)

    def read_datapoints(self):
        yield from self.underlying.read_datapoints()

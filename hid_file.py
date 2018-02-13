from enum import Enum
import struct
import lzma
import gzip
import builtins
import os
from DataPoint import DataPoint

class HIDType(Enum):
    FIXED = 0
    FLOAT32 = 1
    FLOAT64 = 2

    @staticmethod
    def get_entry_format_str(hid_type):
        if hid_type == HIDType.FLOAT32:
            return '<qqffff'
        elif hid_type == HIDType.FLOAT64:
            return '<qqdddd16x'
        raise ValueError("invalid HIDType")

    @staticmethod
    def get_header_format_str():
        return '<ccccIqI44x'

    @staticmethod
    def decode_data_type(data_type):
        if data_type == 0:
            return HIDType.FIXED
        if data_type == 1:
            return HIDType.FLOAT32
        if data_type == 2:
            return HIDType.FLOAT64
        else:
            raise ValueError("invalid data_type for HIDType")

    @staticmethod
    def encode_data_type(hid_type):
        if hid_type == HIDType.FIXED:
            return 0
        if hid_type == HIDType.FLOAT32:
            return 1
        if hid_type == HIDType.FLOAT64:
            return 2
        else:
            raise ValueError("invalid data_type for HIDType")

class HIDFile:

    def __init__(self, path, permissions, hid_type=HIDType.FLOAT32):
        self.path = path
        self.permissions = permissions
        self.fp = None
        self.data_type = None
        self.version = None
        self.length = None

    def __iter__(self):
        # we have to assume that the file is open at this point. if it isn't our logic is wrong
        self.fp.seek(0)
        self.unpack_header(self.fp.read(64))

    def __next__(self):
        entry_size = 32 if self.data_type == HIDType.FLOAT32 else 64
        data = self.fp.read(entry_size)
        if not data:
            raise StopIteration
        return DataPoint(packed=data, hid_type=self.data_type)

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

    def write_datapoints(self, data_points):
        #there's a very real possibility that we're reading from and writing to the same file
        #so we need to copy the entire data_points and then seek back to the beginning
        data_points = list(data_points)
        self.length = len(data_points)
        self.fp.seek(0)
        self.fp.write(self.pack_header())
        for dp in data_points:
            self.fp.write(dp.pack())

    def unpack_header(self, bytes_str):
        _, _, _, _, self.version, self.length, t = struct.unpack(HIDType.get_header_format_str(), bytes_str)
        self.data_type = HIDType.decode_data_type(t)

    def pack_header(self):
        bytes_str = struct.pack(HIDType.get_header_format_str(),'d','i','h','.', self.version, self.length, self.data_type)
        return bytes_str

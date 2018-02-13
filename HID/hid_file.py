from enum import Enum
import struct
import lzma
import gzip
import builtins
import os

from utils import *
from DataPoint import DataPoint
from HID import HIDType


class HIDFile:

    def __init__(self, path, permissions, hid_type=HIDType.FLOAT32):
        self.path = path
        self.permissions = permissions
        self.fp = None
        self.hid_type = hid_type
        self.version = 0
        self.length = None

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

    def write_datapoints(self, data_points, hid_type):
        #there's a very real possibility that we're reading from and writing to the same file
        #so we need to copy the entire data_points and then seek back to the beginning
        data_points = list(data_points)
        self.length = len(data_points)
        self.fp.seek(0)
        self.fp.write(self.pack_header())
        out_bytes = b''
        for dp in data_points:
            out_bytes += dp.pack(hid_type)
            if len(out_bytes) >= 65536:
                self.fp.write(out_bytes)
                out_bytes = b''
        self.fp.write(out_bytes)

    def read_datapoints(self):
        self.fp.seek(0)
        self.unpack_header(self.fp.read(64))
        while True:
            data = self.fp.read(65536)
            if not data:
                break
            for bytes_str in chunks(data,32):
                yield DataPoint(packed=bytes_str)

    def unpack_header(self, bytes_str):
        _, _, _, _, self.version, self.length, t = struct.unpack(HIDType.get_header_format_str(), bytes_str)
        self.hid_type = HIDType.decode_hid_type(t)

    def pack_header(self):
        dt = HIDType.encode_hid_type(self.hid_type)
        bytes_str = struct.pack(HIDType.get_header_format_str(),b'd',b'i',b'h',b'.', self.version, self.length, dt)
        return bytes_str

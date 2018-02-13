from enum import Enum

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
    def decode_hid_type(hid_type):
        if hid_type == 0:
            return HIDType.FIXED
        if hid_type == 1:
            return HIDType.FLOAT32
        if hid_type == 2:
            return HIDType.FLOAT64
        else:
            raise ValueError("invalid hid_type for HIDType")

    @staticmethod
    def encode_hid_type(hid_type):
        if hid_type == HIDType.FIXED:
            return 0
        if hid_type == HIDType.FLOAT32:
            return 1
        if hid_type == HIDType.FLOAT64:
            return 2
        else:
            raise ValueError("invalid hid_type for HIDType")
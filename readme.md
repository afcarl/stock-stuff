requires python >= 3.3 (might require more than that though)

alpha_vantage pandas twilio cbor2 numpy pytest

.hid file format - historical intraday

.hid is a binary file format for storing intraday data, primarily

minutes, volume, open, high, low, close

either fixed point, 32 bit floating point, or 64 bit floating point numbers can be used for decimals

fixed point uses 2 32 bit numbers to represent a decimal number

fixed point decimal numbers are 64 bits in length composed of 2 32 bit signed integer little endian
bytes 0 - 3 - integer part
bytes 4 - 7 - fractional part

byte ordering is always little endian

for 64 bit floats or fixed point:

    entries are organized into 64 byte groups, like so

    bytes 0 - 7   minutes - 64 bit signed integer little endian representing minutes from epoch time
    bytes 8 - 15  volume  - 64 bit signed integer little endian representing the volume
    bytes 16 - 23 open    - 64 bit signed fixed pair / float decimal little endian representing the opening price
    bytes 24 - 31 high    - 64 bit signed fixed pair / float decimal little endian representing the highest price
    bytes 32 - 39 low     - 64 bit signed fixed pair / float decimal little endian representing the lowest price
    bytes 40 - 47 close   - 64 bit signed fixed pair / float decimal little endian representing the closing price
    bytes 48 - 63 reserved for padding and/or future expansion

    entries must be 64 byte aligned

for 32 bit floats:
    entries are organized into 32 byte groups, like so

    bytes 0 - 7   minutes - 64 bit signed integer little endian representing minutes from epoch time
    bytes 8 - 15  volume  - 64 bit signed integer little endian representing the volume
    bytes 16 - 19 open    - 32 bit float decimal little endian representing the opening price
    bytes 20 - 23 high    - 32 bit float decimal little endian representing the highest price
    bytes 24 - 27 low     - 32 bit float decimal little endian representing the lowest price
    bytes 28 - 31 close   - 32 bit float decimal little endian representing the closing price

    entries must be 32 byte aligned

(version 0) entries start immediately after the header
gaps between entries are not allowed

file has a 64 byte header
byte 0    - 'd'
byte 1    - 'i'
byte 2    - 'h'
byte 3    - '.'
bytes 4-7  - version - 32 bit unsigned integer little endian. currently only valid value is 0
bytes 8-15 - length  - 64 bit signed integer little endian representing the number or datapoints in this file
byte 16-19  - data_type - 32 bit unsigned integer little endian. 0 for fixed point. 1 for 32 bit float. 2 for 64 bit float
bytes 20-63 - reserved
requires python >= 3.3 (might require more than that though)

alpha_vantage pandas twilio cbor2

.hid file format - historical intraday

.hid is a binary file format for storing intraday data, primarily

minutes, open, high, low, close, volume

either fixed point or floating point numbers can be used for decimals

floating point version uses one 64 bit float to represent a decimal number
fixed point uses 2 32 bit numbers to represent a decimal number

fixed point decimal numbers are 64 bits in length composed of 2 32 bit signed integer little endian
bytes 0 - 3 - integer part
bytes 4 - 7 - fractional part

byte ordering is always little endian

entries are organized into 64 byte groups, like so

bytes 0 - 7   minutes - 64 bit signed integer little endian representing minutes from epoch time
bytes 8 - 15  open    - 64 bit signed fixed pair / float decimal little endian representing the opening price
bytes 16 - 23 high    - 64 bit signed fixed pair / float decimal little endian representing the highest price
bytes 24 - 31 low     - 64 bit signed fixed pair / float decimal little endian representing the lowest price
bytes 32 - 39 close   - 64 bit signed fixed pair / float decimal little endian representing the closing price
bytes 40 - 47 volume  - 64 bit signed integer little endian representing the volme
bytes 48 - 63 reserved for padding and/or future expansion

entries must be 64 byte aligned
(version 0) entries start immediately after the header
gaps between entries are not allowed

file has a 64 byte header
byte 0    - 'd'
byte 1    - 'i'
byte 2    - 'h'
byte 3    - '.'
bytes 4-7 - version - 32 bit unsigned integer little endian. currently only valid value is 0
bytes 8   - length - 15 - 64 bit signed integer little endian representing the number or datapoints in this file
byte 16   - data_type  1 byte bool. 0 if using floating point numbers. 1 if using fixed point
bytes 17-63 - reserved
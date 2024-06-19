from tools import *
import os
import sys

os.chdir(os.path.dirname(__file__))

target = 'read'
if len(sys.argv) > 1:
    target = sys.argv[1]

q = b'"Friendship, like the immortality of the soul, is too good to be believed." - Ralph Waldo Emerson'

"""
encoding:
"""

def encode(message: bytes):
    size = len(message)
    try:
        enc_size = size.to_bytes (bytes_per_size)
    except OverflowError:
        raise RuntimeError('cannot fit message size to one byte')
    
    buffer = bytearray (enc_size)

    buffer[0:bytes_per_size] = enc_size
    buffer[bytes_per_size:bytes_per_size + size] = message

    return buffer

"""
decoding
"""

from secret import decode

"""
actual 'main
"""


if target == 'write':
    bmp = BitMap.from_file('res/1.bmp')
    
    try:
        message = sys.argv[2]
    except:
        message = q


    enc_message = encode (message)


    bmp.set_row(0, enc_message)

    bmp.put('out/1.bmp')
    print ('message encoded!')

else:
    bmp = BitMap.from_file('out/1.bmp')

    first_row = bmp.get_row(0)

    message = decode (bytearray(first_row))

    print (message)


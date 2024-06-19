from tools import *
import os
import sys

os.chdir(os.path.dirname(__file__))

target = 'read'
if len(sys.argv) > 1:
    target = sys.argv[1]

q = b'"Fine words and an insinuating appearance are seldom associated with true virtue" - Confucius'

"""
encoding:
"""


def pack(message: bytes):
    size = len(message)
    try:
        pack_size = size.to_bytes(bytes_per_size)
    except OverflowError:
        raise RuntimeError('cannot fit message size to one byte')

    buffer = bytearray(bytes_per_size + size)

    buffer[:bytes_per_size] = pack_size
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
    bmp = BitMap.from_file('res/3.bmp')

    try:
        message = sys.argv[2]
    except:
        message = q

    packed = pack(message)

    pure_bits = convert_bytearray_to_bits(packed)

    raw_canvas = bmp.get_canvas()

    for idx in range(len(pure_bits)):
        idx_with_offset = idx * lsb_offset

        enc_byte = set_bit(
            raw_canvas[idx_with_offset], pure_bits[idx])
        raw_canvas[idx_with_offset] = enc_byte

    bmp.set_canvas(raw_canvas)

    bmp.put('out/3.bmp')
    print('message encoded!')

else:
    bmp = BitMap.from_file('out/3.bmp')
    message = decode(bmp)
    print(message)

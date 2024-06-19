from tools import *
import os
import sys

os.chdir(os.path.dirname(__file__))

target = 'read'
if len(sys.argv) > 1:
    target = sys.argv[1]

q = b'"A creative man is motivated by the desire to achieve, not by the desire to beat others." - Ayn Rand'

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

    buffer[0:bytes_per_size] = pack_size
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
    bmp = BitMap.from_file('res/4.bmp')

    try:
        message = sys.argv[2]
    except:
        message = q

    packed = pack(message)

    
    pure_bits = convert_bytearray_to_bits (packed)

    pure_bits_ecc = repeat_list_items (pure_bits, ecc_count)

    raw_canvas = bmp.get_canvas()

    for idx in range(len(pure_bits_ecc)):
        idx_with_offset = idx * lsb_offset
        
        enc_byte = set_bit(
            raw_canvas [idx_with_offset], pure_bits_ecc[idx])
        raw_canvas [idx_with_offset] = enc_byte

    bmp.set_canvas (raw_canvas)

    bmp.put('out/4.bmp')
    print('message encoded!')

else:
    bmp = BitMap.from_file('out/4.bmp')
    message = decode (bmp)
    print (message)



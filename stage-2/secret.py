from tools import *

def decode(bmp: BitMap):
    raw_canvas = bmp.get_canvas ()


    message_size_length = bytes_per_size * 8
    bits_message_size = get_bit_from_bytearray (
        raw_canvas [0: message_size_length]
    )

    bytes_message_size = pack_bits_into_bytearray (bits_message_size)

    message_length = int.from_bytes (bytes_message_size)

    print ('message length: ', message_length)

    offset = message_size_length
    bits_message = get_bit_from_bytearray (
        raw_canvas [offset: offset + message_length * 8]
    )
    bytes_message = pack_bits_into_bytearray (bits_message)

    return bytes_message

from tools import *

def decode(bmp: BitMap):
    raw_canvas = bmp.get_canvas ()


    message_size_length = bytes_per_size * 8 * ecc_count
    bits_message_size_ecc = get_bit_from_bytearray (
        raw_canvas [0: message_size_length * lsb_offset: lsb_offset]
    )

    bits_message_size = round_list_items_by_n (bits_message_size_ecc, ecc_count)

    bytes_message_size = pack_bits_into_bytearray (bits_message_size)

    message_length = int.from_bytes (bytes_message_size)

    print ('message length: ', message_length)

    offset = message_size_length * lsb_offset
    
    bits_message_ecc = get_bit_from_bytearray (
        raw_canvas [offset: offset + message_length * 8 * lsb_offset * ecc_count: lsb_offset]
    )
    bits_message = round_list_items_by_n (bits_message_ecc, ecc_count)

    bytes_message = pack_bits_into_bytearray (bits_message)

    return bytes_message

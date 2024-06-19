from tools import *
import os
import sys

os.chdir(os.path.dirname(__file__))

target = 'read'
if len(sys.argv) > 1:
    target = sys.argv[1]

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


# def encode(raw_canvas: bytearray, bits: list) -> bytearray:

#     for idx in range(len(bits)):
#         idx_with_offset = idx * lsb_offset

#         enc_byte = set_bit(
#             raw_canvas[idx_with_offset], pure_bits_ecc[idx])
#         raw_canvas[idx_with_offset] = enc_byte

#     return raw_canvas


"""
decoding
"""

from secret import decode

"""
actual 'main
"""


if target == 'write':

    with open('res/input.jpg', 'rb') as i:
        message = i.read()
    print ('message size:', len(message))

    packed = pack(message)

    pure_bits = convert_bytearray_to_bits(packed)

    pure_bits_ecc = repeat_list_items(pure_bits, ecc_count)

    to_encode_size = len(pure_bits_ecc)
    print('bits to encode:', to_encode_size)

    print('required canvas size:', to_encode_size * lsb_offset)


    current_bit_position = 0
    path_canvas_dir = 'res/canvas/'
    path_out_dir = 'out/messages/'
    for file_name in sorted(os.listdir(path_canvas_dir)):
        bmp = BitMap.from_file(os.path.join(path_canvas_dir, file_name))

        print('file:', os.path.basename(file_name))
        print('size:', bmp.header.row_image_size)

        bits_to_encode = int(
            bmp.header.row_image_size / lsb_offset)

        print('bytes to use (to encode bits count):', bits_to_encode)
        print('to encode bytes count:', bits_to_encode / 8)


        raw_canvas = bmp.get_canvas()

        current_pure_bits_ecc_cut = pure_bits_ecc[
            current_bit_position: 
            current_bit_position + bits_to_encode]
            
        for idx in range(len(current_pure_bits_ecc_cut)):
            idx_with_offset = idx * lsb_offset

            enc_byte = set_bit(
                raw_canvas[idx_with_offset], current_pure_bits_ecc_cut[idx])
            raw_canvas[idx_with_offset] = enc_byte
        
        bmp.set_canvas(raw_canvas)
        output_file_name = os.path.join(path_out_dir, 'm_' + file_name)
        bmp.put(output_file_name)

        
        current_bit_position = current_bit_position + bits_to_encode
        print('bytes left to encode:', to_encode_size - current_bit_position)

        # print (current_pure_bits_ecc_cut[-20:])
        # decoded = full_decode (bmp)
        # ld = len(decoded)
        # p = packed [
        #     iteration * ld:
        #     iteration * ld + ld]
        # print (len(decoded))
        # if p != decoded:
        #     err = find_bytearray_difference (p, decoded)
        #     print (err)
        # iteration = iteration + 1

        

    if current_bit_position < to_encode_size:
        raise Exception('not enouth canvas to encode!')
    print('message encoded!')

else:
    path_messages_dir = 'out/messages/'

    decode (path_messages_dir)
    # fully_decoded = bytearray()

    # for message_name in sorted(os.listdir(path_messages_dir)):
    #     bmp = BitMap.from_file(os.path.join(path_messages_dir, message_name))
        
    #     found_bytes = full_decode (bmp)
    #     print ('found bytes:', len(found_bytes))
    #     fully_decoded.extend(found_bytes)
    
    # message_size = int.from_bytes(fully_decoded[0:bytes_per_size])

    # print ('message size:', message_size)

    # with open ('out/result.jpg', 'wb+') as o:
    #     o.write (fully_decoded [
    #         bytes_per_size: bytes_per_size + message_size
    #     ])


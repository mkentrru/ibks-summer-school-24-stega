from tools import *

def full_decode(bmp: BitMap):
    raw_canvas = bmp.get_canvas()

    used_bytes = raw_canvas[0:bmp.header.row_image_size: lsb_offset]

    bits_message_ecc = get_bit_from_bytearray(used_bytes)
    bits_message = round_list_items_by_n(bits_message_ecc, ecc_count)

    decoded = pack_bits_into_bytearray(bits_message)

    return decoded

def decode (path_messages_dir):
    
    fully_decoded = bytearray()

    for message_name in sorted(os.listdir(path_messages_dir)):
        bmp = BitMap.from_file(os.path.join(path_messages_dir, message_name))
        
        found_bytes = full_decode (bmp)
        print ('found bytes:', len(found_bytes))
        fully_decoded.extend(found_bytes)
    
    message_size = int.from_bytes(fully_decoded[0:bytes_per_size])

    print ('message size:', message_size)

    with open ('out/result.jpg', 'wb+') as o:
        o.write (fully_decoded [
            bytes_per_size: bytes_per_size + message_size
        ])
from tools import *
def decode (buffer: bytearray):
    size = int.from_bytes(buffer [:bytes_per_size])
    message = buffer[bytes_per_size: bytes_per_size + size] 
    return message

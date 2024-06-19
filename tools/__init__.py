global BitMap
from .bmp import BITMAP as BitMap
from .bmp import pRGB

from .bmp import gen_pRGB_row

from ctypes import *
import os

"""
constants
"""
bytes_per_size = 4
lsb_offset = 0x10
ecc_count = 3

def convert_bytearray_to_bits(byte_array):
    return [int(bit) for byte in byte_array for bit in f'{byte:08b}']


def get_bit_from_bytearray(byte_array):
    return [byte & 1 for byte in byte_array]


def set_bit(byte, value, bit_position=0):
    mask = 1 << bit_position
    byte &= ~mask
    if value:
        byte |= mask
    return byte


def pack_bits_into_bytearray(bits):
    packed = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        while len(byte) < 8:
            byte.append(0)
        packed.append(int(''.join(map(str, byte)), 2))
    return packed

def repeat_list_items(lst, N):
    return [item for item in lst for _ in range(N)]

def round_list_items_by_n(lst, n):
    return [round(sum(lst[i:i+n]) / n) for i in range(0, len(lst), n)]

def find_bytearray_difference(byte_array1, byte_array2):
    return next((i for i, (a, b) in enumerate(zip(byte_array1, byte_array2)) if a != b), None)



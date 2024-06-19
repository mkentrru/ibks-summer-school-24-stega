from ctypes import *


class pRGB (LittleEndianStructure):
    _fields_ = [
        ('b', c_uint8),
        ('g', c_uint8),
        ('r', c_uint8)]
    _pack_ = 1

    def __init__(self, *args, **kw) -> None:
        r = kw.get('r', args[0])
        g = kw.get('g', args[1])
        b = kw.get('b', args[2])
        super().__init__(r=r, g=g, b=b)

    def red(self): return self.r
    def green(self): return self.g
    def blue(self): return self.b


def calculate_row_size(width, bbp):
    return ((int)((bbp * width + 31) / 32)) * 4


def gen_pRGB_row(width):
    row_size = calculate_row_size(width, 24)
    padding = row_size - width * 3

    class pRGB_row (LittleEndianStructure):
        _fields_ = [
            ('pixels', pRGB * width),
            ('padding', c_uint8 * padding)
        ]
        _pack_ = 1

        def __init__(self) -> None:
            super().__init__()

        def __getitem__(self, idx) -> pRGB:
            return self.pixels[idx]

        def __setitem__(self, k, v: pRGB):
            self.pixels[k] = v

        @classmethod
        def from_bytes(cls, buffer: bytearray, v: bytes, pos:int=0):
            length = min (len(buffer), len(v))
            buffer [:length] = v
            return pRGB_row.from_buffer_copy(buffer)
        

    return pRGB_row()


class BITMAPINFOHEADER(LittleEndianStructure):
    _fields_ = [
        ('B', c_uint8),
        ('M', c_uint8),

        ('len', c_uint32),

        ('res01', c_uint32),

        ('offset', c_uint32),

        # BITMAPINFOHEADER
        ('len_header', c_uint32),  # = 12
        ('w', c_int32),
        ('h', c_int32),
        ('len_colorplanes', c_uint16),  # = 1
        ('bpp', c_uint16),  # = 24

        ('compression', c_uint32),  # = 0

        ('row_image_size', c_uint32),
        ('resolution_x', c_int32),
        ('resolution_y', c_int32),
        ('len_colorplane', c_uint32),  # =0
        ('len_important', c_uint32),  # =0

    ]
    _pack_ = 1

    def __init__(self, **kw) -> None:

        w = kw['w']
        h = kw['h']

        super().__init__(w=w, h=h)
        self.B = ord('B')
        self.M = ord('M')

        self.offset = sizeof(self)
        self.bpp = 24

        self.row_size = calculate_row_size(self.w, self.bpp)

        self.len = self.offset + self.row_size * self.h

        self.len_header = 40
        self.len_colorplanes = 1
        self.compression = 0
        self.row_image_size = self.row_size * self.h
        self.resolution_x = 0xb13
        self.resolution_y = 0xb13

        self.len_colorplane = 0
        self.len_important = 0


class BITMAP ():
    def __init__(self, header, rows=None) -> None:
        self.w = header.w
        self.h = header.h
        self.bpp = 24

        self.row_size = calculate_row_size(self.w, self.bpp)
        self.header = header

        self.rows = [gen_pRGB_row(self.w) for _ in range(self.h)]

    def height(self): return self.h
    def width(self): return self.w
    def row_bytes_length(self): return self.row_size

    def get_row(self, idx: int):
        return self.rows[idx]

    def set_row(self, idx, value: bytes, pos:int=0):
        row_bytes = bytearray (self.rows[idx])
        self.rows[idx] = gen_pRGB_row(self.width()).from_bytes(row_bytes, value, pos)

    def get_pixel(self, x: int, y: int):
        if x < self.width() and y < self.height():
            return self.get_row(y)[x]

    def get_pixel(self, pos):
        x = pos % self.width()
        y = pos // self.height()
        return self.get_pixel(x, y)

    def get_canvas (self) -> bytearray:
        res = bytearray().join (
            [bytearray(row) for row in self.rows]
        )
        return res

    def set_canvas (self, value: bytearray):
        for idx in range (self.height()):
            start = idx * self.row_size
            end = start + self.row_size
            self.set_row(idx, value [start: end])

    @classmethod
    def simple(cls, w: int = 250, h: int = 250):
        return cls(
            BITMAPINFOHEADER(w=w, h=h))

    @classmethod
    def from_file(cls, path):
        with open(path, 'rb') as i:
            bytes_header = i.read(
                sizeof(BITMAPINFOHEADER))
            header = BITMAPINFOHEADER.from_buffer_copy(
                bytes_header)

            bmp = BITMAP(header)
            for idx in range(bmp.height()):
                bytes_row = i.read(bmp.row_bytes_length())
                bmp.set_row(idx, bytes_row)

            return bmp

    def bytes_header(self):
        return bytes(self.header)

    def bytes_row(self, idx):
        return bytes(self.rows[idx])

    def iter_rows(self):
        class RowsIterator ():
            def __init__(self, bmp: BITMAP) -> None:
                self.bmp = bmp

            def __iter__(self):
                self.idx = 0
                return self

            def __next__(self):
                if self.idx < self.bmp.h:
                    res = self.bmp.bytes_row(self.idx)
                    self.idx = self.idx + 1
                    return res
                raise StopIteration
        return RowsIterator(self)

    def draw_pixel(self, x, y, color: pRGB):
        if x < self.w and y < self.h:
            self.rows[y][x] = color

    def draw_rect(self, x, y, dx, dy, pRGB):
        for x1 in range(x, x + dx):
            for y1 in range(y, y + dy):
                self.draw_pixel(x1, y1, pRGB)

    def put(self, path: str):
        with open(path, 'bw+') as o:
            o.write(self.bytes_header())
            for row in self.iter_rows():
                o.write(row)

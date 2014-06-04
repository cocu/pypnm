from pypnm.dummy_numpy import DummyNumpy

try:
    import numpy
except ImportError:
    numpy = DummyNumpy


class InvalidFormat(BaseException): pass


class TemplateMode(object):
    is_binary_input = False
    pixcel_function = lambda self, i: 255 * i / self.max_pixel_value
    data_bit_size = 8  # if binary mode

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.max_pixel_value = 255


    def _gen_iter(self, data):
        def gen_iter_split_space(data):
            while data:
                while data and data[0] == ' ':
                    data = data[1:]
                res = ''
                while data and data[0] != ' ':
                    res += data[0]
                    data = data[1:]
                if res.isdigit():
                    value = int(res) % (self.max_pixel_value + 1 )
                    if self.pixcel_function is not None:
                        value = self.pixcel_function(value)
                    yield value

        def gen_iter_one_bytes(data):
            ONE_BYTE = 8
            if self.max_pixel_value == 8:
                for x in data:
                    yield ord(x)
            elif self.max_pixel_value == 2:
                for x in data:
                    for y in bin(x)[2:].rjust(ONE_BYTE, 0):
                        yield int(y)

        if self.is_binary_input:
            return gen_iter_one_bytes(data)
        else:
            return gen_iter_split_space(data)

    def _parse_rect(self, iterator, color_num=1):
        if color_num == 1:
            array = numpy.empty(( self.height, self.width))
        else:
            array = numpy.empty(( color_num, self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                if color_num == 1:
                    try:
                        array[y][x] = next(iterator)
                    except StopIteration:
                        raise InvalidFormat('less data size: (%d,%d)' % (x, y))
                else:
                    for c in range(color_num):
                        try:
                            array[y][x][c] = next(iterator)
                        except StopIteration:
                            raise InvalidFormat('less data size: (%d,%d)' % (x, y))
        return array

    def _parse(self, it):
        # over write here
        pass

    def parse(self, data):
        it = self._gen_iter(data)
        try:
            return self._parse(it)
        except StopIteration:
            raise InvalidFormat('less data size')


class ParserP1(TemplateMode):
    is_binary_input = False
    pixcel_function = lambda self, i: 255 * i  # input data is {0,1} convert to 8bit world

    def _parse(self, it):
        self.max_pixel_value = 1

        return self._parse_rect(it)


class ParserP2(TemplateMode):
    is_binary_input = False

    def _parse(self, it):
        self.max_pixel_value = next(it)
        return self._parse_rect(it)


class ParserP3(TemplateMode):
    is_binary_input = False

    def _parse(self, it):
        self.max_pixel_value = next(it)
        return self._parse_rect(it, 3)


class ParserP4(ParserP1):
    is_binary_input = True
    pass


class ParserP5(ParserP2):
    is_binary_input = True
    pass


class ParserP6(ParserP3):
    is_binary_input = True
    pass


supported_format = {
    'P1': ParserP1,
    'P2': ParserP2,
    'P3': ParserP3,
    # 'P4': ParserP4,
    # 'P5': ParserP5,
    # 'P6': ParserP6,
}


def _gen_iter(idata):
    """
    :type data:str
    """
    data = idata
    for _ in range(3):
        data = data.lstrip(' ')
        idx = data.index(' ')
        yield data[:idx]
        data = data[idx:]
    yield data


def parse2array(string):
    data = ' '.join([x[:x.find('#')] if '#' in x else x for x in string.splitlines()])
    i = _gen_iter(data)
    try:
        format_type = next(i)
        width = next(i)
        height = next(i)
    except IndexError:
        raise InvalidFormat('format or width or height is not exists')
    
    if width and width.isdigit() and height and height.isdigit():
        width = int(width)
        height = int(height)
    else:
        raise InvalidFormat('widht and height is not integer: w:%s h:%s' % (width, height))
    if width <= 0 or height <= 0:
        raise InvalidFormat('width or height is invlaid')

    if format_type not in supported_format:
        raise InvalidFormat('the format is not supported: %s' % format_type)

    data = next(i)

    parser = supported_format[format_type](width, height)
    res = parser.parse(data)
    return res
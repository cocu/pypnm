import unittest


class TestParse(unittest.TestCase):
    def setUp(self):
        from pypnm.parser import parse
        import numpy

        self.target_func = parse
        self.numpy = numpy

    def test_p1(self):
        data = '\n'.join([
            'P1',
            '# This is an example bitmap of the letter "J"',
            '6 10',
            '0 0 0 0 1 0',
            '0 0 0 0 1 0',
            '0 0 0 0 1 0',
            '0 0 0 0 1 0',
            '0 0 0 0 1 0',
            '0 0 0 0 1 0',
            '1 0 0 0 1 0',
            '0 1 1 1 0 0',
            '0 0 0 0 0 0',
            '0 0 0 0 0 0'
        ])

        array = self.target_func(data)
        res = self.numpy.array([
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]) * 255
        self.assertTrue((array == res).all())

    def test_p2(self):
        data = '\n'.join([
            'P2',
            '# Shows the word "FEEP" (example from Netpbm man page on PGM)',
            '24 7',
            '15',
            '0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0',
            '0  3  3  3  3  0  0  7  7  7  7  0  0 11 11 11 11  0  0 15 15 15 15  0',
            '0  3  0  0  0  0  0  7  0  0  0  0  0 11  0  0  0  0  0 15  0  0 15  0',
            '0  3  3  3  0  0  0  7  7  7  0  0  0 11 11 11  0  0  0 15 15 15 15  0',
            '0  3  0  0  0  0  0  7  0  0  0  0  0 11  0  0  0  0  0 15  0  0  0  0',
            '0  3  0  0  0  0  0  7  7  7  7  0  0 11 11 11 11  0  0 15  0  0  0  0',
            '0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0',
        ])

        array = self.target_func(data)

        res = self.numpy.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 3, 3, 3, 0, 0, 7, 7, 7, 7, 0, 0, 11, 11, 11, 11, 0, 0, 15, 15, 15, 15, 0],
            [0, 3, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 15, 0, 0, 15, 0],
            [0, 3, 3, 3, 0, 0, 0, 7, 7, 7, 0, 0, 0, 11, 11, 11, 0, 0, 0, 15, 15, 15, 15, 0],
            [0, 3, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 7, 7, 7, 7, 0, 0, 11, 11, 11, 11, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]) * 255 / 15
        self.assertTrue((array == res).all())

    def test_p3(self):
        data = '\n'.join([
            'P3',
            '# The P3 means colors are in ASCII, then 3 columns and 2 rows, then 255 for max color, then RGB triplets',
            '3 3',
            '255',
            '255 0 0',
            '0 255 0',
            '0 0 255',
            '255 255 0',
            '0 255 255',
            '255 0 255',
            '0 0 0',
            '127 127 127',
            '255 255 255',
        ])

        array = self.target_func(data)

        res = self.numpy.array([
            [
                [255, 0, 0],
                [0, 255, 0],
                [0, 0, 255],
            ],
            [
                [255, 255, 0],
                [0, 255, 255],
                [255, 0, 255],
            ],
            [
                [0, 0, 0],
                [127, 127, 127],
                [255, 255, 255],
            ],
        ])
        self.assertTrue((array == res).all())

    # def test_p6(self):
    #     data = b'P6\n# The P6 means colors are in binary, '\
    #            'then 255 for max color, then RGB triplets\n#\n3 3\n255\n\xff\x00\x00\x00' \
    #            '\xff\x00\x00\x00\xff\xff\xff\x00\x00\xff\xff\xff\x00\xff\x00\x00\x00\x7f' \
    #            '\x7f\x7f\xff\xff\xff'
    #     data = data.decode('utf-8')
    #     
    #     array = self.target_func(data)
    #     res = self.numpy.array([
    #         [
    #             [255, 0, 0],
    #             [0, 255, 0],
    #             [0, 0, 255],
    #         ],
    #         [
    #             [255, 255, 0],
    #             [0, 255, 255],
    #             [255, 0, 255],
    #         ],
    #         [
    #             [0, 0, 0],
    #             [127, 127, 127],
    #             [255, 255, 255],
    #         ],
    #     ])
    #     self.assertTrue((array == res).all())
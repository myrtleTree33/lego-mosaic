import numpy as np
import cv2
from filters import *
import errno
import os
import base64
import json


class Image(object):
    """docstring for Image."""

    def __init__(self, length):
        super(Image, self).__init__()
        self.length = length
        self.img = None

    def load_file(self, filepath):
        self.img = cv2.imread(filepath)
        # Nonexistent input file
        if self.img is None:
            raise EnvironmentError(
                errno.ENOENT, os.strerror(errno.ENOENT), filepath)
        self.img = cv2.resize(self.img, (self.length, self.length))
        return self

    def load_str(self, img_str_base64):
        img_str = base64.b64decode(img_str_base64)
        nparr = np.fromstring(img_str, dtype=np.uint8)
        self.img = cv2.imdecode(nparr, 1)  # cv2.IMREAD_COLOR in OpenCV 3.1
        # self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB) # flip BGR to RGB
        self.img = cv2.resize(self.img, (self.length, self.length))
        return self

    def dump_str_base64(self, file_format):
        dump = cv2.imencode('.' + file_format, self.img)[1].tostring()
        return base64.b64encode(dump)

    def apply_filter(self, filter):
        filter.apply(self)
        return self

    def show(self):
        cv2.imshow('output', self.img)
        cv2.waitKey(0)
        return self

    def save_file(self, filepath):
        cv2.imwrite(filepath, self.img)
        return self

    def generate_instructions(self, tile_size):
        result = {
            'colorList': []
        }
        pic = self.img
        histogram = {}
        for y in range(2, len(pic), tile_size):
            for x in range(2, len(pic[y]), tile_size):
                (r, g, b) = pic[y - 1][x - 1]
                if (r, g, b) not in histogram:
                    print 'a'
                    histogram[(r, g, b)] = 0
                histogram[(r, g, b)] = histogram[(r, g, b)] + 1

        for k, v in histogram.iteritems():
            result['colorList'].append({
                'color': str(k),
                'qty': v
            })

        print json.dumps(result)
        return json.dumps(result)


def main():
    img = Image(48)
    img.load_file('logo17.jpg')
    img \
        .apply_filter(QuantizeFilter(7)) \
        .apply_filter(ConstrainPaletteFilter('Lego-colors-palette-2010.gpl.csv')) \
        .apply_filter(BuildMapFilter(12)) \
        .show()


if __name__ == '__main__':
    main()

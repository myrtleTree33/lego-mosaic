import numpy as np
import cv2
import csv
from filters import *
import errno
import os


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
            raise EnvironmentError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
        self.img = cv2.resize(self.img, (self.length, self.length))
        return self


    def apply_filter(self, filter):
        filter.apply(self)
        return self


    def show(self):
        cv2.imshow('output', self.img)
        cv2.waitKey(0)
        return self


    def save_file(self, filepath):
        cv2.imwrite(filepath,self.img)
        return self


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

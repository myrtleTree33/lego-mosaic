import numpy as np
import cv2
import csv

class Filter(object):
    """docstring for Filter."""
    def __init__(self):
        super(Filter, self).__init__()


    def apply(self, img):
        raise NotImplementedError("Subclass must implement abstract method")


class MyFilter(Filter):
    """docstring for MyFilter."""
    def __init__(self):
        super(MyFilter, self).__init__()


    def apply(self, target):
        print 'called'


class QuantizeFilter(Filter):
    """docstring for MyFilter."""
    def __init__(self, num_clusters):
        super(QuantizeFilter, self).__init__()
        self.num_clusters = num_clusters


    def apply(self, target):
        Z = target.img.reshape((-1,3))
        # convert to np.float32
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret,label,center = cv2.kmeans(Z,self.num_clusters,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        # Now convert back into uint8, and make original image
        quantize_centers = np.uint8(center)
        res = quantize_centers[label.flatten()]
        target.img = res.reshape((target.img.shape))


class ConstrainPaletteFilter(Filter):
    """docstring for ConstrainPaletteFilter."""
    def __init__(self, palette_filepath):
        super(ConstrainPaletteFilter, self).__init__()
        self.palette = []
        self._build_palette(palette_filepath)


    def _build_palette(self, csv_file):
        print csv_file
        with open(csv_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            reader.next()
            for row in reader:
                b,g,r = row[:3]
                self.palette.append([int(r),int(g),int(b)])


    def _fit_palette(self, pic):

        def _nearestColor(pixel, palette):
            MAX_DIFF = pow(pow(255, 2) * 3, .5)
            nearest_color, smallest_val = 0, MAX_DIFF
            r,g,b = pixel
            for p in palette:
                r2, g2, b2 = p
                val = pow(pow(r - r2, 2) + pow(g - g2, 2) + pow(b - b2, 2), .5)
                if (smallest_val > val):
                    # print smallest_val
                    smallest_val = val
                    nearest_color = p
            return nearest_color

        h,w = len(pic[0]), len(pic)
        output = np.zeros((w,h,3), np.uint8)
        for y, row in enumerate(pic):
            for x, color in enumerate(row):
                a = _nearestColor(pic[y][x], self.palette)
                output[y][x] = a
        return output


    def apply(self, target):
        self.img = self._fit_palette(target.img)


class BuildMapFilter(Filter):
    """docstring for BuildMapFilter."""
    def __init__(self, grid_size):
        super(BuildMapFilter, self).__init__()
        self.grid_size = grid_size


    def _draw_grid(self, pic, grid_size, grid_color):
        h,w = len(pic[0]), len(pic)
        for y in xrange(0, h, grid_size):
            cv2.line(pic, (0, y), (w, y), grid_color)
        for x in xrange(0, w, grid_size):
            cv2.line(pic, (x, 0), (x, h), grid_color)


    def apply(self, target):
        grid_size = self.grid_size
        pic = target.img
        # Create a black image
        h,w = len(pic[0]) * grid_size, len(pic) * grid_size
        output = np.zeros((w,h,3), np.uint8)
        for y, row in enumerate(pic):
             for x, color in enumerate(row):
                 r,g,b = color
                 r = int(r)
                 g = int(g)
                 b = int(b)
                 cv2.rectangle(output,
                    (x * grid_size, y * grid_size),
                    ((x + 1) * grid_size,(y + 1) * grid_size)
                    ,(r,g,b),-2)

        self._draw_grid(output, grid_size, (200,200,200))
        self._draw_grid(output, grid_size * 10, (0,0,200))
        target.img = output

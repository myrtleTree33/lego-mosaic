import pkg_resources
import csv

class Color_Generator(object):
    """docstring for Color_Generator."""
    def __init__(self):
        super(Color_Generator, self).__init__()
        self.palettes = {}


    def load_palette(self, palette_name, csv_filepath):
        palette = []
        with open(csv_filepath, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            reader.next()
            for row in reader:
                b, g, r = row[:3]
                palette.append([int(r), int(g), int(b)])
        self.palettes[palette_name] = palette


    def get_palette(self, palette_name):
        if palette_name not in self.palettes:
            raise Exception('No palette scheme with given key=%s found' % palette_name)
        return self.palettes[palette_name]

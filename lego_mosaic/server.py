import zerorpc
from image import Image
import os
import glob
from color_generator import Color_Generator
from filters import *

IP = 'tcp://0.0.0.0'
PORT = '4000'


class MosaicServer(object):
    """
    Creates a server for generating Mosaics as a service, using zerorpc.
    """

    def __init__(self):
        super(MosaicServer, self).__init__()
        color_generator = Color_Generator()

        def load_color_palettes():
            pattern = os.path.dirname(__file__) + '/resources/*.csv'
            for filename in glob.iglob(pattern):
                palette_name = os.path.splitext(os.path.basename(filename))[0]
                color_generator.load_palette(palette_name, filename)
        load_color_palettes()
        self.color_generator = color_generator

    def generate_mosaic(self, input_base64, num_clusters, img_length, tile_size, palette_name):
        """
        Generates a mosaic from  a base64 filedata string.
        """
        img = Image(img_length)
        img \
            .load_str(input_base64) \
            .apply_filter(QuantizeFilter(num_clusters)) \
            .apply_filter(ConstrainPaletteFilter(self.color_generator, palette_name)) \
            .apply_filter(BuildMapFilter(tile_size))
        output_base64 = img.dump_str_base64('png')
        print 'image generated..'
        return output_base64


def main():
    server = zerorpc.Server(MosaicServer())
    server.bind(IP + ":" + PORT)
    server.run()


if __name__ == '__main__':
    main()

import zerorpc
from image import Image
from filters import *

IP = 'tcp://0.0.0.0'
PORT = '4000'

class MosaicServer(object):
    """
    Creates a server for generating Mosaics as a service, using zerorpc.
    """
    def __init__(self):
        super(MosaicServer, self).__init__()

    def generate_mosaic(self, input_base64, num_clusters, img_length, tile_size):
        """
        Generates a mosaic from  a base64 filedata string.
        """
        print 'called'
        img = Image(img_length)
        img \
        .load_str(input_base64) \
        .apply_filter(QuantizeFilter(num_clusters)) \
        .apply_filter(ConstrainPaletteFilter('Lego-colors-palette-2010.gpl.csv')) \
        .apply_filter(BuildMapFilter(tile_size))
        output_base64 = img.dump_str_base64('png')
        return output_base64


def main():
    server = zerorpc.Server(MosaicServer())
    server.bind(IP + ":" + PORT)
    server.run()


if __name__ == '__main__':
    main()

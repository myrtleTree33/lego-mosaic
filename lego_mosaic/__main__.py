import zerorpc
import argparse
from filters import *
from image import Image
from color_generator import Color_Generator
from server import MosaicServer
import pkg_resources


IP = 'tcp://0.0.0.0'
PORT = '4000'

def run_server(ip, port):
    # Run a server if specified
    address = ip + ":" + port
    server = zerorpc.Server(MosaicServer())
    print 'Running server at %s' % address
    server.bind(address)
    server.run()


def main():
    parser = argparse.ArgumentParser(description='Convert your pictures into a a Lego mosaic.')
    # parser.add_argument('--server', action='run_server', help='If toggled, displays output to screen')
    parser.add_argument('--server', nargs='?', const=True, type=bool, default=False, help='Starts a ZMQ server')
    parser.add_argument('input_filename', metavar='input_filename', type=str, nargs='?', help='The input image to convert')
    parser.add_argument('output_filename', metavar='output_filename', type=str, const='out.jpg', default='out.jpg', nargs='?', help='The output image to save to')
    parser.add_argument('--show', nargs='?', const=True, type=bool, default=False, help='If toggled, displays output to screen')
    parser.add_argument('--size', nargs='?', const=5, type=int, default=5, help='The rendering length of each tile.')
    parser.add_argument('--length', nargs='?', const=48, type=int, default=48, help='The length of each mosaic.')
    parser.add_argument('--num_clusters', nargs='?', const=7, type=int, default=7, help='Number of color clusters to quantize')
    # parser.add_argument('--show', dest='accumulate', action='store_const',
                    #    const=sum, default=max,
                    #    help='sum the integers (default: find the max)')

    args = parser.parse_args()

    start_server = args.server
    if (start_server):
        run_server(IP, PORT)


    input_filename = args.input_filename
    output_filename = args.output_filename
    tile_size = args.size
    n = args.num_clusters
    img_length = args.length

    resource_path = 'Lego-colors-palette-2010.gpl.csv'
    csv_filepath = pkg_resources.resource_filename(__name__, resource_path)

    color_generator = Color_Generator()
    color_generator.load_palette('colors2010', csv_filepath)

    img = Image(img_length)
    img.load_file(input_filename) \
    .apply_filter(QuantizeFilter(n)) \
    .apply_filter(ConstrainPaletteFilter(color_generator, 'colors2010')) \
    .apply_filter(BuildMapFilter(tile_size)) \
    .save_file(output_filename)


    if args.show:
        img.show()




if __name__ == '__main__':
    main()

from filters import *
from image import Image
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert your pictures into a a Lego mosaic.')
    parser.add_argument('input_filename', metavar='input_filename', type=str, nargs='+', help='The input image to convert')
    parser.add_argument('output_filename', metavar='output_filename', type=str, nargs='+', help='The output image to save to')
    parser.add_argument('--show', nargs='?', const=True, type=bool, default=False)
    parser.add_argument('--size', nargs='?', const=5, type=int, default=5, help='The rendering length of each tile.')
    parser.add_argument('--length', nargs='?', const=48, type=int, default=48, help='The length of each mosaic.')
    parser.add_argument('--num_clusters', nargs='?', const=7, type=int, default=7, help='Number of color clusters to quantize')
    # parser.add_argument('--show', dest='accumulate', action='store_const',
                    #    const=sum, default=max,
                    #    help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print args

    input_filename = args.input_filename[0]
    output_filename = args.output_filename[0]
    tile_size = args.size
    n = args.num_clusters
    img_length = args.length

    img = Image(img_length)
    img.load_file(input_filename)
    img \
    .apply_filter(QuantizeFilter(n)) \
    .apply_filter(ConstrainPaletteFilter('Lego-colors-palette-2010.gpl.csv')) \
    .apply_filter(BuildMapFilter(tile_size)) \

    if args.show:
        img.show()




if __name__ == '__main__':
    main()

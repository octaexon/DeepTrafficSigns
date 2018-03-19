import argparse
import os
from PIL import Image


''' convert_images.py

    converts images to desired format with desired properties
'''

__author__ = 'James Ryan'
__copyright__ = 'Copyright 2018'
__credits__ = ['James Ryan']
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'James Ryan' 
__email__ = 'octaexon@gmail.com'
__status__ = 'Development'


import utilities.parser_utilities as parserutils


EXTENSION_LOOKUP = {'JPEG': 'jpg'}

def _valid_extension(arg):
    if not EXTENSION_LOOKUP.get(arg, None):
        msg = ('invalid format : \'{}\'; '.format(arg) 
                + ' '.join(EXTENSION_LOOKUP.keys())
                + ' supported')
        raise argparse.ArgumentTypeError(msg)
    return arg


def _nohidden_listdir(path):
    return [os.path.join(path, filename) for filename in os.listdir(path) if not filename.startswith('.')]



def _convert_path(input_path, output_dir, output_format):
    return os.path.join(output_dir,                                 # join output directory
                os.path.basename(                                   # remove input directory
                    os.path.splitext(input_path)[0]                 # remove old extension
                        + '.' + EXTENSION_LOOKUP[output_format]))   # add new extension




def convert(input_dir, output_dir, output_format, scale):

    os.makedirs(output_dir, exist_ok=True)

    for input_path in _nohidden_listdir(input_dir):

        output_path = _convert_path(input_path, output_dir, output_format)

        image = Image.open(input_path)

        output_size = tuple(int(scale * coordinate) for coordinate in image.size)

        image.thumbnail(output_size)

        image.save(output_path, output_format)



if __name__ == "__main__":
    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', 
                        dest='input_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to input images directory')
    parser.add_argument('-o', '--output-dir',
                        dest='output_dir',
                        type=parserutils.absolute_writable_path,
                        required=True,
                        help='path to output images directory')
    parser.add_argument('-f', '--format',
                        dest='output_format',
                        type=_valid_extension,
                        default='JPEG',
                        help='output format for images')
    parser.add_argument('-s', '--scale',
                        dest='scale',
                        default=1.0,
                        type=parserutils.bounded_float(lower=0.0),
                        help='factor to scale each coordinate')

    args, _ = parser.parse_known_args()

    # change working directory to project root directory
    PROJECT_ROOT = '..'
    os.chdir(PROJECT_ROOT)

    convert(**vars(args))

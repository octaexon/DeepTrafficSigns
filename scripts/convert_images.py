import argparse
import os
from PIL import Image
import pandas as pd


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


PROJECT_ROOT = '..'

PROPERTIES_CSV = 'properties.csv'

EXTENSION_LOOKUP = {'JPEG': 'jpg'}


def _valid_extension(arg):
    if not EXTENSION_LOOKUP.get(arg, None):
        msg = ('invalid format : \'{}\'; '.format(arg) 
                + ' '.join(EXTENSION_LOOKUP.keys())
                + ' supported')
        raise argparse.ArgumentTypeError(msg)
    return arg

def _read_input_image_properties(directory):
    properties_path = os.path.join(directory, PROPERTIES_CSV)
    if os.path.exists(properties_path):
        return pd.read_csv(properties_path)
    return None


def _list_images(path):
    return [os.path.join(path, filename) for filename in os.listdir(path) 
            if not (filename.startswith('.') or filename.endswith('.csv'))]



def _convert_path(input_path, output_dir, output_format):
    return os.path.join(output_dir,                                 # join output directory
                os.path.basename(                                   # remove input directory
                    os.path.splitext(input_path)[0]                 # remove old extension
                        + '.' + EXTENSION_LOOKUP[output_format]))   # add new extension




def convert(input_dir, output_dir, output_format, scale):

    os.makedirs(output_dir, exist_ok=True)

    input_image_properties = _read_input_image_properties(input_dir)

    #TODO: could validate that the properties file has same number of lines
    # as listed images 

    output_image_properties = []

    for input_path in _list_images(input_dir):

        output_path = _convert_path(input_path, output_dir, output_format)

        image = Image.open(input_path)

        output_size = tuple(int(scale * coordinate) for coordinate in image.size)

        image.thumbnail(output_size)

        image.save(output_path, output_format)

        # compute scale of output image with respect to original
        if input_image_properties is None:
            output_scale = scale
        else:
            output_scale = scale * input_image_properties.scale[input_image_properties.filename == input_path].iloc[0]

        output_image_properties.append([output_path, *output_size, output_scale])

    output_image_properties = pd.DataFrame(output_image_properties, columns=['filename', 'width', 'height', 'scale'])

    output_image_properties.to_csv(os.path.join(output_dir, PROPERTIES_CSV), index=False)







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
    os.chdir(PROJECT_ROOT)

    convert(**vars(args))

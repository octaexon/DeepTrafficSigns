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


import utilities.metadata_utilities as metautils
import utilities.parser_utilities as parserutils


PROJECT_ROOT = '..'

PROPERTIES_CSV = 'properties.csv'

EXTENSION_LOOKUP = {'JPEG': 'jpg'}



def _list_images(path):
    ''' list image files only from some images directory

        Paraameter

        path: str
            path to images directory


        Returns

        list of image filenames


        Note:
            Assumes that there are only hidden, csv or image files
    '''
    return [os.path.join(path, filename) for filename in os.listdir(path) 
            if not (filename.startswith('.') or filename.endswith('.csv'))]



def _convert_path(input_path, output_dir, output_ext):
    ''' convert input path to output path, only file basename
        without extension is invariant

        Parameters

        input_path: str
            input file path

        output_dir: str
            path to output directory

        output_ext: str
            extension for output file


        Returns

        output file path
    '''
    return os.path.join(output_dir,                                 # join output directory
                os.path.basename(                                   # remove input directory
                    os.path.splitext(input_path)[0]                 # remove old extension
                        + '.' + output_ext))                        # add new extension




def convert(input_dir, output_dir, output_format, scale):
    ''' convert input to output images, rescaling and reformating

        Parameters

        input_dir: str
            path to input image directory

        output_dir: str
            path to output image directory

        output_format: str
            output image format for PIL library

        scale: float
            factor to rescale each coordinate
    '''
    os.makedirs(output_dir, exist_ok=True)

    input_image_properties = metautils.read_image_properties(os.path.join(input_dir, PROPERTIES_CSV))

    #TODO: could validate that the properties file has same number of lines
    # as listed images 
    output_image_properties = []

    for input_path in _list_images(input_dir):

        output_path = _convert_path(input_path, output_dir, EXTENSION_LOOKUP[output_format])

        image = Image.open(input_path)

        output_size = tuple(int(scale * coordinate) for coordinate in image.size)

        image.thumbnail(output_size)

        image.save(output_path, output_format)

        # compute scale of output image with respect to original
        if input_image_properties is None:
            output_scale = scale
        else:
            output_scale = (scale * 
                    input_image_properties.scale[input_image_properties.filename == input_path]
                                           .iloc[0])

        output_image_properties.append([output_path, *output_size, output_scale])

    output_image_properties = pd.DataFrame(output_image_properties, 
                                           columns=['filename', 'width', 'height', 'scale'])

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
                        type=parserutils.valid_format(EXTENSION_LOOKUP.keys()),
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

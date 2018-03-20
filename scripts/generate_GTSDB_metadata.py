import argparse
import os
import re
import pandas as pd
from PIL import Image

''' generate_GTSDB_metadata.py

    generate standarised metadata from raw files and imagees
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
DEFAULT_SCALE = 1.0


def generate_metadata(images_path,
                      image_metadata_path, 
                      class_metadata_path, 
                      output_metadata_path):
    ''' generate image and class metadata

        Parameters

        images_path: str
            path to jpg images directory

        image_metadata_path: str
            path to raw images metadata

        class_metadata_path: str
            path to raw class metadata

        output_metadata_path: str
            path to write generated metadata
    '''
    # load raw image and bounding box metadata
    metadata = pd.read_csv(image_metadata_path,
                           sep=';',
                           header=None,
                           names=['filename', 'xmin', 'ymin', 
                                  'xmax', 'ymax', 'class_id'])

    # create absolute file paths
    # TODO: jpg extension is hardcoded here
    metadata.filename = (metadata.filename
                                 .str.replace('ppm', 'jpg')
                                 .apply(lambda x: os.path.join(images_path, x)))

    # additional image metadata, if available
    image_metadata = metautils.read_image_properties(os.path.join(images_path, PROPERTIES_CSV))


    if image_metadata is None:
        # generate additional image metadata
        image_metadata = pd.DataFrame([[path, *Image.open(path).size, DEFAULT_SCALE] 
                                       for path in metadata.filename],
                                      columns=['filename', 'width', 'height', 'scale'])

    metadata = metadata.merge(image_metadata, on='filename')

    # account for current and previooous scaling
    metadata[['xmin', 'ymin', 'xmax', 'ymax']] = (
            metadata.apply(lambda x: x[['xmin', 'ymin', 'xmax', 'ymax']] * x['scale'], axis=1)
                    .astype('int64'))

    # load raw class metadatẅa and process
    with open(class_metadata_path, 'r') as fd:
        lines = fd.readlines()

    classes = []
    for line in lines:
        match = re.match('^(\d{1,2}) = (.+\()(.+)', line)
        if match:
            class_id = int(match.group(1))
            description = match.group(2).rstrip(' (')
            category = match.group(3).rstrip(')')
            classes.append([class_id, description, category])

    class_metadata = pd.DataFrame(classes,
                                  columns=['class_id', 'description', 'category'])

    metadata = metadata.merge(class_metadata, on='class_id')

    metadata.to_csv(output_metadata_path, index=False)



if __name__ == '__main__':
    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', 
                        dest='input_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to input images directory')

    args, _ = parser.parse_known_args()

    IMAGES_PATH = args.input_dir

    METADATA_PATH = os.path.realpath(os.path.join(PROJECT_ROOT, 'data/sign_detection_data/metadata'))

    CLASS_METADATA_PATH = os.path.join(METADATA_PATH, 'README.txt')
    IMAGE_METADATA_PATH = os.path.join(METADATA_PATH, 'raw_metadata.txt')
    OUTPUT_METADATA_PATH = os.path.join(METADATA_PATH, 'metadata.csv')

    generate_metadata(IMAGES_PATH, 
                      IMAGE_METADATA_PATH, 
                      CLASS_METADATA_PATH, 
                      OUTPUT_METADATA_PATH)

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


PROJECT_ROOT = '..'


def generate_metadata(images_path,
                      image_metadata_path, 
                      class_metadata_path, 
                      output_metadata_path):
    ''' generate image and class metadata

        Parameters

        images_path: str
            path to jpg images directory

        metadata_path: str
            path to metadata directory

        image_metadata_path: str
            path to raw images metadata

        class_metadata_path: str
            path to raw class metadata

        output_metadata_path: str
            path to write generated metadata
    '''
    metadata = pd.read_csv(image_metadata_path,
                           sep=';',
                           header=None,
                           names=['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class_id'])

    metadata.filename = (metadata.filename
                                 .str.replace('ppm', 'jpg')
                                 .apply(lambda x: os.path.join(images_path, x)))


    metadata[['width', 'height']] = pd.DataFrame([Image.open(path).size for path in metadata.filename])


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
    # change working directory to project root directory
    os.chdir(PROJECT_ROOT)

    METADATA_PATH = 'data/sign_detection_data/metadata'
    IMAGES_PATH = 'data/sign_detection_data/images/jpg_thumbnails'

    CLASS_METADATA_PATH = os.path.join(METADATA_PATH, 'README.txt')
    IMAGE_METADATA_PATH = os.path.join(METADATA_PATH, 'raw_metadata.txt')
    OUTPUT_METADATA_PATH = os.path.join(METADATA_PATH, 'metadata.csv')

    generate_metadata(IMAGES_PATH, 
                      IMAGE_METADATA_PATH, 
                      CLASS_METADATA_PATH, 
                      OUTPUT_METADATA_PATH)

import argparse
import os
import pandas as pd


''' create_labelmap.py

    converts image and class metadata stored 
    in csv format to a label map
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

LABEL_MAP_FILENAME_TEMPLATE = 'top_{top}_label_map.pbtxt'

LABEL_MAP_TEMPLATE = 'item {{\n    id: {label}\n    name: \'{description}\'\n}}'


def metadata2labelmap(metadata):
    ''' csv to label map converter

        Parameters

        metadata: pandas.DataFrame
            metadata must contain columns: label, class_id, description, category


        Returns

        label_map: str
            label map for the "top" classes with fields:
                id: metadata.label             <- class identifier (*)
                name: metadata.description     <- class display (*)
                original_id: metadata.class_id <- original class id in class metadata
                category: metadata.category    <- category for sign

        Notes
        (*) signifies that this is a label map field required by 
            object detection api

        id parameters for label map must be unique and greater than 0, since
        0 is reserved as the id for the null class
    '''

    return (metadata[['label', 'description', 'class_id', 'category']]
                    .drop_duplicates()
                    .sort_values(by='label')
                    .apply(lambda x: LABEL_MAP_TEMPLATE.format(**x.to_dict()), axis=1)
                    .str.cat(sep='\n\n'))



def process_metadata(metadata_path, dst_dir, top):
    ''' ingest metadata, call converter, write label map

        Parameters

        metadata_path: str
            path to csv file

        dst_dir: str
            path to output directory

        top: False or int
            positive int indicating "top" most frequent classes
            to select
            False to indicate that all classes should be selected
    '''
    metadata = pd.read_csv(metadata_path)

    metadata = metautils.add_labels(metadata)

    top, metadata = metautils.get_top_metadata(top, metadata)
 
    label_map_path = metautils.create_output_path(dst_dir, LABEL_MAP_FILENAME_TEMPLATE, top=top)

    with open(label_map_path, 'w') as fd:
        # create label map parameters
        label_map = metadata2labelmap(metadata)
        # write to disk
        fd.write(label_map)




if __name__ == "__main__":
    # prescribed metadata file
    METADATA_CSV = 'metadata.csv'

    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metadata-dir', 
                        dest='metadata_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to metadata directory')
    parser.add_argument('-t', '--top', 
                        dest='top', 
                        default=False, 
                        type=parserutils.bounded_int(lower=0),
                        help='-t 5 means top 5 labels in terms of frequency \
                              should be included in label map')

    args, _ = parser.parse_known_args()

    metadata_path = os.path.join(args.metadata_dir, METADATA_CSV)

    # change working directory to project root directory
    os.chdir(PROJECT_ROOT)

    process_metadata(metadata_path,
                     args.metadata_dir,
                     args.top)

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


LABEL_MAP_TEMPLATE = 'item {{\n    id: {id}\n    name: \'{description}\'\n}}'


def metadata2labelmap(metadata):
    ''' csv to label map converter

        Parameters

        metadata: pandas.DataFrame
            metadata must contain columns: id, class_id, description, category


        Returns

        label_map: str
            label map for the "top" classes with fields:
                id: metadata.id                <- identifier of class within tensorflow
                name: metadata.description     <- textual name of class

        id parameters for label map must be unique and begin at 1, since
        0 is reserved as the id for the null class
    '''
    return (metadata[['id', 'description', 'class_id', 'category']]
                    .drop_duplicates()
                    .sort_values(by='id')
                    .apply(lambda x: LABEL_MAP_TEMPLATE.format(**x.to_dict()), axis=1)
                    .str.cat(sep='\n\n'))



def process_metadata(metadata_path, selected_metadata_path, label_map_path, class_list, top):
    ''' ingest metadata, call converter, write label map

        Parameters

        metadata_path: str
            path to csv file

        selected_metadata_path: str
            path to csv file

        output_dir: str
            path to output directory

        class_list: None or list(int)
            list of class ids

        top: None or int
            positive int indicating "top" most frequent classes
            to select
    '''
    metadata = pd.read_csv(metadata_path)

    selected_metadata = metautils.select_metadata(metadata, class_list, top)

    with open(label_map_path, 'w') as fd:
        # create label map parameters
        label_map = metadata2labelmap(selected_metadata)
        # write to disk
        fd.write(label_map)

    selected_metadata.to_csv(selected_metadata_path, index=False)




if __name__ == "__main__":
    # prescribed metadata file
    METADATA_CSV = 'metadata.csv'
    SELECTED_METADATA_CSV = 'selected_metadata.csv'
    LABEL_MAP_PBTXT = 'label_map.pbtxt'

    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metadata-dir', 
                        dest='metadata_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to metadata directory')
    parser.add_argument('-d', '--data-dir', 
                        dest='data_dir', 
                        type=parserutils.absolute_writable_path,
                        required=True,
                        help='path to data directory')
    parser.add_argument('-t', '--top', 
                        dest='top', 
                        type=parserutils.bounded_int(lower=1),
                        help='-t 5 means top 5 labels in terms of frequency \
                              should be included in label map')
    parser.add_argument('-l', '--list',
                       dest='class_list',
                       nargs='+',
                       type=parserutils.bounded_int(lower=0),
                       help='list of non-negative class ids')

    args, _ = parser.parse_known_args()

    metadata_path = os.path.join(args.metadata_dir, METADATA_CSV)
    selected_metadata_path = os.path.join(args.metadata_dir, SELECTED_METADATA_CSV)
    label_map_path = os.path.join(args.data_dir, LABEL_MAP_PBTXT)

    # change working directory to project root directory
    os.chdir(PROJECT_ROOT)

    process_metadata(metadata_path,
                     selected_metadata_path,
                     label_map_path,
                     args.class_list,
                     args.top)

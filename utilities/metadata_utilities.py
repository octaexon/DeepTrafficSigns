import os
import pandas as pd

''' metadata_utilities.py

    convenience functions for other modules
'''

__author__ = 'James Ryan'
__copyright__ = 'Copyright 2018'
__credits__ = ['James Ryan']
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'James Ryan' 
__email__ = 'octaexon@gmail.com'
__status__ = 'Development'


def load_metadata(class_metadata_path, image_metadata_path):
    ''' metadata loader

        Parameters

        class_metadata_path: str
            required column: class_id

        image_metadata_path: str
            required column: class_id


        Returns

        merged metadata: pandas.DataFrame
    '''
    return pd.merge(pd.read_csv(class_metadata_path), 
                    pd.read_csv(image_metadata_path),
                    on='class_id')



def create_output_path(dst_dir, template, **kwargs):
    ''' 
        Parameters

        dst_dir: str
            destination directory

        template: str
            template for filename

        **kwargs:  
            parameters to complete template


        Returns

        label_map_path: str
    '''
    # ensure existence of destination directory 
    os.makedirs(dst_dir, exist_ok=True)

    return os.path.join(dst_dir, template.format(**kwargs))



def add_labels(metadata):
    ''' add a "label" column to some metadata by ranking frequency
        of the associated "class_id"

        Parameters

        metadata: pandas.DataFrame
            required column: class_id


        Returns

        labeled_metadata: pandas.DataFrame
    '''
    return (metadata.groupby('class_id')
                    .size()
                    .rank(method='first', ascending=False)  
                    .astype(int)
                    .to_frame(name='label')
                    .merge(metadata, left_index=True, right_on='class_id'))



def get_top_metadata(top, metadata):
    ''' get valid top and top metadata based on label

        Parameters

        top: False or int
            positive int indicating number of classes to select
            to select
            False to indicate that all classes should be selected

        metadata: pandas.DataFrame
            image/class metadata
            required columns: class_id, label


        Returns

        (valid_top, top_metadata): tuple(int, pandas.DataFrame)
            valid_top is a positive integer less than the total number of classes
            top_metadata is the "top" ranked classes as indicated "label" column

    '''
    nr_classes_occurring = metadata.class_id.unique().size
    if not top or top > nr_classes_occurring:
        top = nr_classes_occurring

    return top, metadata.query('label <= @top')

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



def read_image_properties(properties_path):
    ''' reads image properties file if it exists

        Parameter

        properties_path: str
            path to properties csv file


        Returns

        pandas.Dataframe or None if file is non-existent
    '''
    if os.path.exists(properties_path):
        return pd.read_csv(properties_path)
    return None



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



def select_metadata(metadata, top):
    ''' add an "id" column to some metadata by ranking frequency
        of the associated "class_id"

        Parameters

        metadata: pandas.DataFrame
            required column: class_id

        top: positive int
            "top" most frequent classes to "id"


        Returns

        pandas.DataFrame
            subselection of metadata corresponding to "top"
            most frequent classes
    '''
    nr_classes_occurring = metadata.class_id.unique().size
    if not top or top > nr_classes_occurring:
        top = nr_classes_occurring

    return (metadata.groupby('class_id')
                    .size()
                    .rank(method='first', ascending=False)  
                    .astype(int)
                    .to_frame(name='id')
                    .query('id <= @top')
                    .merge(metadata, left_index=True, right_on='class_id'))



def get_metadata_for_ids(metadata):
    ''' returns metadata that has been given label map ids

        Parameter

        metadata: pandas.DataFrame
            image metadata
            required column: id


        Return

        pandas.DataFrame
            image metadata with non-null ids
    '''
    return metadata[pd.notnull(metadata.id)]

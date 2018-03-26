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

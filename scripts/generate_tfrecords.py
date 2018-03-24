import argparse
import os
import pandas as pd
import tensorflow as tf
import json

''' generate_tfrecords.py

    generate train and eval tfrecords combining metadata and image data
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

# TODO: sampling is greedy by may still need to check 
# if classes small that there is something in training set
def _train_eval_split(metadata, train_frac, random_state=1):
    ''' stratified splitting of metadata into training and evaluation sets

        Parameters

        metadata: pandas.DataFrame
            metadata for image samples
            required column: class_id

        train_frac: float
            fraction of samples to be used for training

        random_state: int
            seed for random sampling


        Returns

        (train_metadata, eval _metadata): tuple of pandas.DataFrames
    '''
    train_metadata = (metadata.groupby('class_id', group_keys=False)
                              .apply(lambda x: x.sample(frac=train_frac, 
                                                        random_state=random_state)))

    eval_metadata = metadata.drop(train_metadata.index)

    return train_metadata, eval_metadata



def _generate_hyperparameter_dict(train_metadata, eval_metadata):
    ''' generates model hyperparameters dictionary

        Parameters

        train_metadata: pandas.DataFrame

        eval_metadata: pandas.DataFrame


        Returns

        dict
            model parameters
    '''
    num_train_classes = len(train_metadata.id.unique())
    num_eval_samples = len(eval_metadata)

    return {'SIZES': 
            {
                'NUM_TRAIN_CLASSES': num_train_classes,
                'NUM_EVAL_SAMPLES': num_eval_samples
            }
           }



# helper functions to streamline tf.train.Feature creation

def _byte_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))



def tf_example_generator(metadata):
    ''' transform jpeg image and its metadata into a tensorflow example

        Parameters

        metadata: pandas.DataFrame
            image, bounding box and class metadata
            required columns: filename, width, height, 
                              xmin, xmax, ymin, ymax,
                              description, id


        Yields

        tensorflow.train.Example
            container amalgamating image data and metadata that may be serialized
            and added to a tensorflow.train.TFRecord
    '''
    for parameters, bbox_metadata in metadata.groupby(['filename', 'width', 'height']):
        filename, width, height = parameters

        with open(filename, 'rb') as fd:
            encoded_data = fd.read()

        # preprocess image and bboxes metadata
        encoded_filename = bytes(os.path.realpath(filename), 'utf-8')
        encoded_format = b'jpg' 

        # rescale bounding box coordinates to [0, 1]
        xmins = (bbox_metadata.xmin / width).tolist()
        xmaxs = (bbox_metadata.xmax / width).tolist()

        ymins = (bbox_metadata.ymin / height).tolist()
        ymaxs = (bbox_metadata.ymax / height).tolist()

        class_labels = bbox_metadata.id.tolist()
        class_texts = bbox_metadata.description.astype('bytes').tolist()

        yield tf.train.Example(
                        features=tf.train.Features(
                            feature={
                                'image/height': _int64_feature([height]),
                                'image/width': _int64_feature([width]),
                                'image/filename': _byte_feature([encoded_filename]),
                                'image/source_id': _byte_feature([encoded_filename]),
                                'image/encoded': _byte_feature([encoded_data]),
                                'image/format': _byte_feature([encoded_format]),
                                'image/object/bbox/xmin': _float_feature(xmins),
                                'image/object/bbox/xmax': _float_feature(xmaxs),
                                'image/object/bbox/ymin': _float_feature(ymins),
                                'image/object/bbox/ymax': _float_feature(ymaxs),
                                'image/object/class/label': _int64_feature(class_labels),
                                'image/object/class/text': _byte_feature(class_texts)
                                }
                            )
                        )


def process_metadata(metadata_path, train_record_path, eval_record_path, parameter_path, train_frac):
    ''' metadata (and images) -> tensorflow record 

        Parameters

        metadata_path: str
            path to csv file

        train_record_path: str
            path to training TFRecord

        eval_record_path: str
            path to evaluation TFRecord

        parameter_path: str
            path to parameter json
            contain number of classes, split information

        train_frac: float
            fraction of samples to be used for training
    '''
    metadata = pd.read_csv(metadata_path)

    train_metadata, eval_metadata = _train_eval_split(metadata, train_frac)

    with open(parameter_path, 'w') as fp:
        hyperparameters = _generate_hyperparameter_dict(train_metadata, eval_metadata)
        json.dump(hyperparameters, fp)

    # construct and write training record
    with tf.python_io.TFRecordWriter(train_record_path) as writer:
        for example in tf_example_generator(train_metadata):
            writer.write(example.SerializeToString())

    # construct and write evaluation record
    with tf.python_io.TFRecordWriter(eval_record_path) as writer:
        for example in tf_example_generator(eval_metadata):
            writer.write(example.SerializeToString())


if __name__ == '__main__':
    # prescribed metadata file
    METADATA_CSV = 'selected_metadata.csv'

    TRAIN_TFRECORD = 'train.tfrecord'
    EVAL_TFRECORD = 'eval.tfrecord'

    PARAMETER_JSON = 'hyperparameters.json'


    #  default train evaluation split ratio
    TRAIN_FRAC = 0.80

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
    parser.add_argument('-l', '--model-dir', 
                        dest='model_dir', 
                        type=parserutils.absolute_writable_path,
                        required=True,
                        help='path to model directory')
    parser.add_argument('-f', '--train-frac', 
                        dest='train_frac', 
                        type=parserutils.bounded_float(lower=0, upper=1),
                        default=TRAIN_FRAC,
                        help='fraction of samples used for training; default={}'.format(TRAIN_FRAC))

    args, _ = parser.parse_known_args()

    metadata_path = os.path.join(args.metadata_dir, METADATA_CSV)
    train_record_path = os.path.join(args.data_dir, TRAIN_TFRECORD)
    eval_record_path = os.path.join(args.data_dir, EVAL_TFRECORD)
    parameter_path = os.path.join(args.model_dir, PARAMETER_JSON)


    # change working directory to project root directory
    os.chdir(PROJECT_ROOT)

    process_metadata(metadata_path,
                     train_record_path,
                     eval_record_path,
                     parameter_path,
                     args.train_frac)

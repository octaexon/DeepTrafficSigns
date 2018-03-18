import argparse
import os
import pandas as pd
import tensorflow as tf

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


# defaults for input and output paths
SCRIPT_DIR = '.'
IMAGE_CSV = os.path.join(SCRIPT_DIR, 'metadata/image_metadata.csv')
CLASS_CSV = os.path.join(SCRIPT_DIR, 'metadata/class_metadata.csv')
DST_DIR = os.path.join(SCRIPT_DIR, 'metadata')

#  default train evaluation split ratio
TRAIN_FRAC = 0.80

TRAIN_TFRECORD_TEMPLATE = 'top_{top}_train.tfrecord'
EVAL_TFRECORD_TEMPLATE = 'top_{top}_eval.tfrecord'


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
                              description, label


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

        class_labels = bbox_metadata.label.tolist()
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


def process_metadata(class_metadata_path, image_metadata_path, dst_dir, top, train_frac):
    ''' metadata (and images) -> tensorflow record 

        Parameters

        class_metadata_path: str
            path to csv file

        image_metadata_path: str
            path to csv file

        dst_dir: str
            directory name for output

        top: False or int
            positive int indicating "top" most frequent classes
            to select
            False to indicate that all classes should be selected

        train_frac: float
            fraction of samples to be used for training
    '''
    metadata = metautils.load_metadata(class_metadata_path, image_metadata_path)

    metadata = metautils.add_labels(metadata)

    top, metadata = metautils.get_top_metadata(top, metadata)

    train_metadata, eval_metadata = _train_eval_split(metadata, train_frac)

    train_record_path = metautils.create_output_path(dst_dir, TRAIN_TFRECORD_TEMPLATE, top=top)
    eval_record_path = metautils.create_output_path(dst_dir, EVAL_TFRECORD_TEMPLATE, top=top)

    # construct and write training record
    with tf.python_io.TFRecordWriter(train_record_path) as writer:
        for tf_example in tf_example_generator(train_metadata):
            writer.write(tf_example.SerializeToString())

    # construct and write evaluation record
    with tf.python_io.TFRecordWriter(eval_record_path) as writer:
        for tf_example in tf_example_generator(eval_metadata):
            writer.write(tf_example.SerializeToString())


if __name__ == '__main__':
    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--class-metadata', dest='class_metadata_path', default=CLASS_CSV,
            help='Input csv file containing class metadata')
    parser.add_argument('-i', '--image-metadata', dest='image_metadata_path', default=IMAGE_CSV,
            help='Input csv file containing image metadata')
    parser.add_argument('-d', '--destination-directory', dest='dst_dir', type=str, default=DST_DIR,
            help='Destination directory for tfrecords')
    parser.add_argument('-t', '--top', dest='top', default=False, type=metautils.positive_int,
            help='-t 5 means top 5 labels in terms of frequency should be included in tfrecords')
    parser.add_argument('-f', '--train-frac', dest='train_frac', type=str, default=TRAIN_FRAC,
            help='train-evaluation split fraction for samples')

    args, _ = parser.parse_known_args()

    process_metadata(**vars(args))

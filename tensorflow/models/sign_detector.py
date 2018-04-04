import os
import cv2
import time
import argparse
import numpy as np
import tensorflow as tf
import multiprocessing as mp


''' sign_detector.py

    detects signs using exports tensorflow graph

    Idea for multiprocessing adapted from:
    https://github.com/datitran/object_detector_app
'''

__author__ = 'James Ryan'
__copyright__ = 'Copyright 2018'
__credits__ = ['James Ryan']
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'James Ryan' 
__email__ = 'octaexon@gmail.com'
__status__ = 'Development'


# TODO: Fix this!!
import sys
sys.path.append(os.path.realpath("../../utilities"))

import parser_utilities as parserutils
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


def _detect_objects(sess, detection_graph, image_array):
    ''' core detection functionality

        Parameters

        sess: tensorflow.Session

        detection_graph: tensflow.Graph

        image_array: numpy.ndarray


        Returns:
            numpy.ndarray annotated image

        Notes:
        This function is documented in the tensorflow object detection api
    '''
    # expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_array_expanded = np.expand_dims(image_array, axis=0)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # detection
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_array_expanded})

    # visualization of the results of a detection
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_array,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)

    return image_array


def _process(input_queue, output_queue, graph_path):
    ''' object detector process

        Parameters

        input_queue: Queue-like object supporting put and get
            should hold numpy.ndarrays

        output_queue: Queue-like object supporting put and get
    '''
    detection_graph = tf.Graph()

    with detection_graph.as_default():
        graph_def = tf.GraphDef()

        with tf.gfile.GFile(graph_path, 'rb') as fd:
            serialized_graph = fd.read()
            graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(graph_def, name='')

    with tf.Session(graph=detection_graph) as sess:
        while True:
            input_image = input_queue.get()
            output_image = _detect_objects(sess, detection_graph, input_image)
            output_queue.put(output_image)



def stream_detector(graph_path, src=0, width=300, height=300, num_processes=1, queue_sz=3): 
    ''' provisions processes for object detection

        Parameters

        src: int
            device id

        width: int
            width to crop frames

        height: int
            height to crop frames

        num_processes: int
            number of detector processes to instantiate

        queue_sz: int
            maximum size of input and output queues
    '''

    input_queue = mp.Queue(maxsize=queue_sz)
    output_queue = mp.Queue(maxsize=queue_sz)

    pool = mp.Pool(num_processes, _process, (input_queue, output_queue, graph_path))

    # launch video crop for better performance
    video_stream = cv2.VideoCapture(src)
    video_stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    video_stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # start timer
    start_time = time.time()
    num_frames = 0

    while True:
        _, input_image = video_stream.read()
        input_queue.put(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))

        output_image = cv2.cvtColor(output_queue.get(), cv2.COLOR_RGB2BGR)
        cv2.imshow('Sign Detector', output_image)

        num_frames += 1

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    stop_time = time.time()

    print('frames/sec: {}'.format(num_frames/(stop_time - start_time)))
    pool.terminate()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    parameters = {'src': 0,
                  'width': 300,
                  'height': 300,
                  'num_processes': 2,
                  'queue_sz': 5}

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--export-dir', 
                        dest='export_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to export directory')
    parser.add_argument('-n', '--num-labels',
                       dest='num_labels',
                       type=parserutils.bounded_int(1, None),
                       required=True,
                       help='number of labels')


    args, _ = parser.parse_known_args()

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    graph_path = os.path.join(args.export_dir, 'output_inference_graph.pb')

    # List of the strings that is used to add correct label for each box.
    label_path = os.path.join(args.export_dir, 'label_map.pbtxt')


    # Loading label map
    label_map = label_map_util.load_labelmap(label_path)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=args.num_labels)
    category_index = label_map_util.create_category_index(categories)


    stream_detector(graph_path, **parameters)

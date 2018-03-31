# exports model checkpoint to inference graph
#
# author = 'James Ryan'
# copyright = 'Copyright 2018'
# credits = ['James Ryan']
# license = 'MIT'
# version = '0.1'
# maintainer = 'James Ryan' 
# email = 'octaexon@gmail.com'
# status = 'Development'


python2 ../tensorflow/models/object_detection/export_inference_graph.py \
        --input_type image_tensor \
        --pipeline_config_path $1 \
        --checkpoint_path $2 \
        --inference_graph_path $3

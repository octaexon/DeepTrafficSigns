# Transfer data from local to cloud

# author = 'James Ryan'
# copyright = 'Copyright 2018'
# credits = ['James Ryan']
# license = 'MIT'
# version = '0.1'
# maintainer = 'James Ryan' 
# email = 'octaexon@gmail.com'
# status = 'Development'

export LOCAL_PROJECT_ROOT=$1

# data transfer
gsutil cp ${LOCAL_PROJECT_ROOT}/data/train.tfrecord ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/data/train.tfrecord
gsutil cp ${LOCAL_PROJECT_ROOT}/data/'eval'.tfrecord ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/data/'eval'.tfrecord
gsutil cp ${LOCAL_PROJECT_ROOT}/data/label_map.pbtxt ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/data/label_map.pbtxt

# model transfer
export REMOTE_PIPELINE_CONFIG=${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/models/mobilenet/pipeline.config

gsutil cp ${LOCAL_PROJECT_ROOT}/models/mobilenet/pipeline.config ${REMOTE_PIPELINE_CONFIG}
gsutil cp ${LOCAL_PROJECT_ROOT}/models/mobilenet/model.ckpt* ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/models/mobilenet/

# list remote directory
echo 
echo Remote filesystem
echo
gsutil ls -r ${REMOTE_PROJECT_ROOT}
echo
echo

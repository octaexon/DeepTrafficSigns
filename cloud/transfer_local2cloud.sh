
# NB: This file can be run from within tensorflow/models/research

# simulation identification
export LOCAL_PROJECT_ROOT=$1

# data transfer
gsutil cp ${LOCAL_PROJECT_ROOT}/data/train.tfrecord ${REMOTE_PROJECT_ROOT}/data/train.tfrecord
gsutil cp ${LOCAL_PROJECT_ROOT}'/data/eval.tfrecord' ${REMOTE_PROJECT_ROOT}'/data/eval.tfrecord'
gsutil cp ${LOCAL_PROJECT_ROOT}/data/label_map.pbtxt ${REMOTE_PROJECT_ROOT}/data/label_map.pbtxt

# model transfer
export REMOTE_PIPELINE_CONFIG=${REMOTE_PROJECT_ROOT}/models/mobilenet/pipeline.config

gsutil cp ${LOCAL_PROJECT_ROOT}/models/mobilenet/cloud_pipeline.config ${REMOTE_PIPELINE_CONFIG}
gsutil cp ${LOCAL_PROJECT_ROOT}/models/mobilenet/model.ckpt* ${REMOTE_PROJECT_ROOT}/models/mobilenet/

# list remote directory
echo 
echo Remote filesystem
echo
gsutil ls -r gs://${BUCKET_NAME}
echo
echo

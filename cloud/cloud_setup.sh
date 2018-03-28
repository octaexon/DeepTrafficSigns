
# NB: This file can be run from within tensorflow/models/research

# could call this script from cloud directory and pass the relative path to
# tensorflow/models/research to the script as a required argument

# initial parameter setup
export GOOGLE_APPLICATION_CREDENTIALS=$1

# GCS bucket creation
#export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export PROJECT_ID=deeptrafficsigns
export BUCKET_NAME=${PROJECT_ID}-mlengine
gsutil mb gs://${BUCKET_NAME}  > /dev/null 2>&1

# simulation identification
export LOCAL_PROJECT_ROOT=$2
export REMOTE_PROJECT_ROOT='gs://'${BUCKET_NAME}/simulation

# data transfer
gsutil cp ${LOCAL_PROJECT_ROOT}/data/train.tfrecord ${REMOTE_PROJECT_ROOT}/data/train.tfrecord
gsutil cp ${LOCAL_PROJECT_ROOT}'/data/eval.tfrecord' ${REMOTE_PROJECT_ROOT}'/data/eval.tfrecord'
gsutil cp ${LOCAL_PROJECT_ROOT}/data/label_map.pbtxt ${REMOTE_PROJECT_ROOT}/data/label_map.pbtxt

# model transfer
export REMOTE_PIPELINE_CONFIG=${REMOTE_PROJECT_ROOT}/models/ssd_mobilenet_v1_coco_2017_11_17/pipeline.config

gsutil cp ${LOCAL_PROJECT_ROOT}/models/ssd_mobilenet_v1_coco_2017_11_17/cloud_pipeline.config ${REMOTE_PIPELINE_CONFIG}
gsutil cp ${LOCAL_PROJECT_ROOT}/models/ssd_mobilenet_v1_coco_2017_11_17/model.ckpt* ${REMOTE_PROJECT_ROOT}/models/ssd_mobilenet_v1_coco_2017_11_17/

# list remote directory
gsutil ls -r gs://${BUCKET_NAME}

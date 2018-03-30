# Setup google cloud storage bucket

#
# author = 'James Ryan'
# copyright = 'Copyright 2018'
# credits = ['James Ryan']
# license = 'MIT'
# version = '0.1'
# maintainer = 'James Ryan' 
# email = 'octaexon@gmail.com'
# status = 'Development'


export TRAIN_JOB_NAME=signs_train_$(date +%s)
export REMOTE_TRAIN_DIR=${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/train
export LOCAL_CONFIG_YAML=${LOCAL_PROJECT_ROOT}/cloud/config.yaml

REGION=us-central1
PACKAGES=dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz
TRAIN_MODULE_NAME=object_detection.train 


gcloud ml-engine jobs submit training ${TRAIN_JOB_NAME} \
    --job-dir ${REMOTE_TRAIN_DIR} \
    --config ${LOCAL_CONFIG_YAML} \
    --region ${REGION} \
    --packages ${PACKAGES} \
    --module-name ${TRAIN_MODULE_NAME}\
    -- \
    --train_dir ${REMOTE_TRAIN_DIR} \
    --pipeline_config_path ${REMOTE_PIPELINE_CONFIG}


export TRAIN_JOB_NAME='signs_train'_$(date +%s)
export LOCAL_CONFIG_YAML=${LOCAL_PROJECT_ROOT}/cloud/config.yaml

export REMOTE_TRAIN_DIR=${REMOTE_PROJECT_ROOT}/train

REGION=us-central1
PACKAGES=dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz
TRAIN_MODULE_NAME=object_detection.train 


gcloud ml-engine jobs submit training ${TRAIN_JOB_NAME} \
    --job-dir ${REMOTE_TRAIN_DIR} \
    --packages ${PACKAGES} \
    --module-name ${TRAIN_MODULE_NAME}\
    --region ${REGION} \
    --config ${LOCAL_CONFIG_YAML} \
    -- \
    --train_dir ${REMOTE_TRAIN_DIR} \
    --pipeline_config_path ${REMOTE_PIPELINE_CONFIG}



export EVAL_JOB_NAME='signs_eval'_$(date +%s)

export REMOTE_EVAL_DIR=${REMOTE_PROJECT_ROOT}'/eval'

REGION=us-central1
PACKAGES=dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz
EVAL_MODULE_NAME='object_detection.eval'

gcloud ml-engine jobs submit training ${EVAL_JOB_NAME}\
    --runtime-version 1.2 \
    --job-dir ${REMOTE_TRAIN_DIR} \
    --packages ${PACKAGES} \
    --module-name ${EVAL_MODULE_NAME} \
    --region ${REGION} \
    --scale-tier BASIC_GPU \
    -- \
    --checkpoint_dir ${REMOTE_TRAIN_DIR} \
    --eval_dir ${REMOTE_EVAL_DIR} \
    --pipeline_config_path ${REMOTE_PIPELINE_CONFIG}

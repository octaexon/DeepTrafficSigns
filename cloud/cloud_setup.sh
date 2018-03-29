
# NB: This file can be run from within tensorflow/models/research


# initial parameter setup
export GOOGLE_APPLICATION_CREDENTIALS=$1

# GCS bucket creation
PROJECT_ID=$(gcloud config list project --format "value(core.project)")
#export PROJECT_ID=deeptrafficsigns
export BUCKET_NAME=${PROJECT_ID}-mlengine
gsutil mb gs://${BUCKET_NAME}

export REMOTE_PROJECT_ROOT='gs://'${BUCKET_NAME}/simulation

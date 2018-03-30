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


# grab credentials from credentials file if provided
export GOOGLE_APPLICATION_CREDENTIALS=$1

# GCS bucket creation
PROJECT_ID=$(gcloud config list project --format "value(core.project)")

export REMOTE_PROJECT_ROOT=gs://${PROJECT_ID}-mlengine
#gsutil mb ${REMOTE_PROJECT_ROOT}

export SIMULATION_ID=simulation_$(date +%s)

echo 
echo Bucket instantiated and simulation id set
echo Configure pipeline with remote direction: ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}
echo

# Transfer training and evaluation data from cloud to local

# author = 'James Ryan'
# copyright = 'Copyright 2018'
# credits = ['James Ryan']
# license = 'MIT'
# version = '0.1'
# maintainer = 'James Ryan' 
# email = 'octaexon@gmail.com'
# status = 'Development'


DESTINATION=${LOCAL_PROJECT_ROOT}/simulations/${SIMULATION_ID}

if [ ! -d ${DESTINATION} ]; then
    mkdir -p ${DESTINATION}
fi

gsutil -m cp -r ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/train ${DESTINATION}
gsutil -m cp -r ${REMOTE_PROJECT_ROOT}/${SIMULATION_ID}/eval ${DESTINATION}

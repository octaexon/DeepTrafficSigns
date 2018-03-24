import argparse
import json
import os

''' setup_pipeline_config.py

    constructs pipeline config file with absolute paths
'''

__author__ = 'James Ryan'
__copyright__ = 'Copyright 2018'
__credits__ = ['James Ryan']
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'James Ryan' 
__email__ = 'octaexon@gmail.com'
__status__ = 'Development'


import utilities.parser_utilities as parserutils

PROJECT_ROOT = '..'

def template2pipeline(parameters_path, hyperparameters_path):
    ''' fills the placeholders in the config file

        Parameter

        parameter_path: str
            json file
            required structure:
                {
                    'PATHS':
                    {
                        'PATH_TO_TEMPLATE_CONFIG': ...,
                        'PATH_TO_PIPELINE_CONFIG': ...,
                        ...
                    }
                }

        hyperparameters_path: str
            json file
            required structure:
                {
                    'SIZES':
                    {
                        ...
                    }
                }
 
    '''
    with open(parameters_path, 'r') as fd:
        parameters = json.load(fd)

    with open(hyperparameters_path, 'r') as fd:
        hyperparameters = json.load(fd)

    # convert relative to absolute paths
    paths = {key: os.path.realpath(path)
                for key, path in parameters['PATHS'].items()}

    # specify size parameters
    sizes = {key: size
                for key, size in hyperparameters['SIZES'].items()}

    template_file = paths['PATH_TO_TEMPLATE_CONFIG']
    with open(template_file, 'r') as fd:
        template_config = fd.read()

    # used the merged dictionaries to fill template
    pipeline_config = template_config % {**paths, **sizes}


    pipeline_file = paths['PATH_TO_PIPELINE_CONFIG']
    # ensure existence of directories
    os.makedirs(os.path.dirname(pipeline_file), exist_ok=True)

    with open(pipeline_file, 'w') as fd:
        fd.write(pipeline_config)


if __name__ == '__main__':
    HYPERPARAMETERS_JSON = 'hyperparameters.json'
    LOCAL_PARAMETERS_JSON = 'local_parameters.json'
    CLOUD_PARAMETERS_JSON = 'cloud_parameters.json'

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-dir', 
                        dest='model_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to model directory')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--local',
                       action='store_true',
                       help='set up pipeline to run locally')
    group.add_argument('-c', '--cloud',
                       action='store_true',
                       help='set up pipeline to run in the cloud')


    args, _ = parser.parse_known_args()

    hyperparameters_path = os.path.join(args.model_dir, HYPERPARAMETERS_JSON)

    if args.local:
        parameters_path = os.path.join(args.model_dir, LOCAL_PARAMETERS_JSON)
    else:
        parameters_path = os.path.join(args.model_dir, CLOUD_PARAMETERS_JSON)

    # change working directory to project root directory
    os.chdir(PROJECT_ROOT)

    template2pipeline(parameters_path, hyperparameters_path)

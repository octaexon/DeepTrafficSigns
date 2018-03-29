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

def template2pipeline(template_path, pipeline_path, hyperparameters_path, project_root):
    ''' fills the placeholders in the config file

        Parameter

        template_path: str
            path to template config file for pipeline
            required placeholder key:
                PROJECT_ROOT

        pipeline_path: str
            path to pipeline config file

        hyperparameters_path: str
            json file
            required structure:
                {
                    'SIZES':
                    {
                        ...
                    }
                }

        project_root: str
            path to project root (local or cloud)
    '''
    with open(hyperparameters_path, 'r') as fd:
        hyperparameters = json.load(fd)

    # specify size parameters
    sizes = {key: size
                for key, size in hyperparameters['SIZES'].items()}

    with open(template_path, 'r') as fd:
        template_config = fd.read()

    # used the merged dictionaries to fill template
    pipeline_config = template_config % {'PROJECT_ROOT': project_root, **sizes}

    # ensure existence of directories
    os.makedirs(os.path.dirname(pipeline_path), exist_ok=True)

    with open(pipeline_path, 'w') as fd:
        fd.write(pipeline_config)


if __name__ == '__main__':
    HYPERPARAMETERS_JSON = 'hyperparameters.json'
    TEMPLATE_FILE = 'template.config'
    PIPELINE_FILE = 'pipeline.config'
    LOCAL_PROJECT_ROOT = os.path.realpath(PROJECT_ROOT)

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-dir', 
                        dest='model_dir', 
                        type=parserutils.absolute_readable_path,
                        required=True,
                        help='path to model directory')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--local',
                       action='store_true',
                       help='setup up to run locally')
    group.add_argument('-c', '--cloud-root',
                       dest='cloud_project_root',
                       type=str,
                       help='path to remote project')


    args, _ = parser.parse_known_args()

    hyperparameters_path = os.path.join(args.model_dir, HYPERPARAMETERS_JSON)
    template_path = os.path.join(args.model_dir, TEMPLATE_FILE)
    pipeline_path = os.path.join(args.model_dir, PIPELINE_FILE)

    if args.local:
        project_root = LOCAL_PROJECT_ROOT
    else:
        project_root = args.cloud_project_root

    # change working directory to project root directory
    os.chdir(PROJECT_ROOT)

    template2pipeline(template_path, pipeline_path, hyperparameters_path, project_root)

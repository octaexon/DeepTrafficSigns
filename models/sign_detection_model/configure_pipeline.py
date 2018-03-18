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



import utilities.metadata_utilities as metautils

# defaults
DEFAULT_PARAMETERS_PATH = './default_parameters.json'


def template2pipeline(parameters_path, **kwargs):
    ''' fills the placeholders in the config file

        Parameter

        parameter_file: str
            json file
            required structure:
                {
                    'SIZES':
                    {
                        ...
                    },
                    'PATHS':
                    {
                        'PATH_TO_TEMPLATE_CONFIG': ...,
                        'PATH_TO_PIPELINE_CONFIG': ...,
                        ...
                    }
                }
    '''
    with open(parameters_path, 'r') as fd:
        parameters = json.load(fd)

    # convert relative to absolute paths
    paths = {key: os.path.realpath(path).format(**kwargs)
                for key, path in parameters['PATHS'].items()}

    # specify size parameters
    sizes = {key: size.format(**kwargs) 
                for key, size in parameters['SIZES'].items()}

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parameters-path', 
                        dest='parameters_path', 
                        default=DEFAULT_PARAMETERS_PATH)
    parser.add_argument('-t', '--top', 
                        dest='top', 
                        type=metautils.positive_int,
                        required=True,
                        help='-t 5 means top 5 labels in terms of frequency \
                              should be included in label map')
    parser.add_argument('-e', '--examples',
                        dest='examples',
                        type=metautils.positive_int,
                        required=True,
                        help='number of samples in evaluation set')

    args = vars(parser.parse_args())


    parameters_path = args.pop('parameters_path')

    template2pipeline(parameters_path, **args)

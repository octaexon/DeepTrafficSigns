import os
import argparse

''' parser_utilities.py

    convenience functions for other modules
'''

__author__ = 'James Ryan'
__copyright__ = 'Copyright 2018'
__credits__ = ['James Ryan']
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'James Ryan' 
__email__ = 'octaexon@gmail.com'
__status__ = 'Development'


def bounded_int(lower=None, upper=None):
    def bounder(arg, lower=lower, upper=upper):
        ''' converts parsed argument string to integer, checking for positivity

            Parameter

            arg: str
                argument string passed from parser to be converted and checked


            Returns

            bounded integer


            Raises

            argparse.ArgumentTypeError
        '''
        try:
            # attempt conversion
            bounded_int = int(arg)

            # check for positivity
            if isinstance(lower, (int, float)) and bounded_int < lower:
                raise ValueError

            if isinstance(upper, (int, float)) and bounded_int > upper:
                raise ValueError

        except ValueError:
            msg = 'invalid bounded int value: {} not in [{}, {}]'.format(arg, lower, upper)
            raise argparse.ArgumentTypeError(msg)

        return bounded_int
    return bounder


def bounded_float(lower=None, upper=None):
    def bounder(arg, lower=lower, upper=upper):
        ''' converts parsed argument string to float, checking for positivity

            Parameter

            arg: str
                argument string passed from parser to be converted and checked


            Returns

            bounded float


            Raises

            argparse.ArgumentTypeError
        '''
        try:
            # attempt conversion
            bounded_float = float(arg)

            # check for positivity
            if isinstance(lower, (int, float)) and bounded_float < lower:
                raise ValueError

            if isinstance(upper, (int, float)) and bounded_float > upper:
                raise ValueError

        except ValueError:
            msg = 'invalid bounded float value: {} not in [{}, {}]'.format(arg, lower, upper)
            raise argparse.ArgumentTypeError(msg)

        return bounded_float
    return bounder



def absolute_readable_path(arg):
    ''' checks path existence

        Parameter

        arg: str
            argument string passed from parser to be validated


        Returns

        arg
            validated absolute path


        Raises

        argparse.ArgumentTypeError
    '''
    if not os.path.exists(arg):
        msg = 'invalid path: \'{}\''.format(arg)
        raise argparse.ArgumentTypeError(msg)
    return os.path.realpath(arg)



def absolute_writable_path(arg):
    ''' converts relative path to absolute path and checks

        Parameter

        arg: str
            argument string passed to parser

        Returns

        arg
            absolute path
    '''
    return os.path.realpath(arg)

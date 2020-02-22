import os
from configparser import ConfigParser


def get_config(option):
    config = ConfigParser()
    directory = os.path.dirname(os.path.realpath(__file__))
    config.read(os.path.join(directory, 'config.ini'))
    return config.get(os.environ.get('SPOT_ENV', 'local'), option)


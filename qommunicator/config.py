from os import environ

from . import __version__

QOMMUNICATOR_VERSION = __version__

SGE_HOST = environ.get('GRIDENGINE_PORT_22_TCP_ADDR')
SGE_USER = environ.get('GRIDENGINE_USER')
SGE_SSH_KEY_PATH = environ.get('GRIDENGINE_SSH_KEY_PATH')
SHARED_VOLUME_PATH = '/shared-volume'

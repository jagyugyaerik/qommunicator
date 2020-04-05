import logging

from qommunicator.config import QOMMUNICATOR_VERSION, SGE_HOST, SGE_USER, \
    SGE_SSH_KEY_PATH, SHARED_VOLUME_PATH
from qommunicator.RemoteClient import RemoteClient

log = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        format='[%(asctime)s] [%(process)d] [%(levelname)s] '
               '%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z',
        level=logging.DEBUG)

    log.info(f"Starting qassembler {QOMMUNICATOR_VERSION}")


if __name__ == '__main__':
    main()

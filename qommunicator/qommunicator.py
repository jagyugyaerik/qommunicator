import logging

from qommunicator.config import QOMMUNICATOR_VERSION

log = logging.getLogger(__name__)


def main(param_file_path: str) -> None:
    logging.basicConfig(
        format='[%(asctime)s] [%(process)d] [%(levelname)s] '
               '%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z',
        level=logging.DEBUG)

    log.info(f"Starting qassembler {QOMMUNICATOR_VERSION}")


if __name__ == '__main__':
    main()

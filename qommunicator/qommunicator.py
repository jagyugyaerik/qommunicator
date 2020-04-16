import logging
import os

import click

from qommunicator.RemoteClient import RemoteClient
from qommunicator.config import QOMMUNICATOR_VERSION, PARAM_FILE_PATH, \
    SGE_HOST, SGE_USER, SGE_SSH_KEY_PATH, SHARED_VOLUME_PATH
from qommunicator.utils import generate_sge_job_params, render_qsub_template,\
    create_qsub_job_file

log = logging.getLogger(__name__)

@click.command()
@click.option('-f',
              '--param-file-path',
              default=PARAM_FILE_PATH,
              help='Location of the parameters')
def main(param_file_path: str) -> None:
    logging.basicConfig(
        format='[%(asctime)s] [%(process)d] [%(levelname)s] '
               '%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z',
        level=logging.DEBUG)

    log.info(f"Starting qassembler {QOMMUNICATOR_VERSION}")
    sge_job_params = generate_sge_job_params(param_file_path)
    log.info(f'Sge job params:{sge_job_params}')
    qsub_job_path = os.path.join(sge_job_params.working_dir_path,
                                 sge_job_params.job_name)
    for env in os.environ.keys():
        log.info(f'{env}: {os.environ[env]}')
    qsub_job = render_qsub_template(sge_job_params)
    create_qsub_job_file(qsub_job_path, qsub_job)

    ssh_client = RemoteClient(host=SGE_HOST,
                              user=SGE_USER,
                              ssh_key_path=SGE_SSH_KEY_PATH,
                              remote_path=SHARED_VOLUME_PATH)
    ssh_client.execute_commands([f'qsub {qsub_job_path}'])


if __name__ == '__main__':
    main()

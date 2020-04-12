import json
import os
from typing import NamedTuple, List, Dict

from jinja2 import FileSystemLoader, Environment

import qommunicator
from qommunicator.config import SHARED_VOLUME_PATH

SgeJobParams = NamedTuple('SgeJobParams',
                          [('job_name', str),
                           ('shell_binary_path', str),
                           ('threads', str),
                           ('que', str),
                           ('golden_binary_path', str),
                           ('golden_reference_path', str),
                           ('input_path', str),
                           ('working_dir_path', str),
                           ('binary_path', str),
                           ('output_path', str),
                           ('error_path', str),
                           ('reference_path', str),
                           ('pipeline', List[Dict[str, str]])])


def generate_sge_job_params(param_file_path):
    with open(param_file_path, 'r') as json_file:
        params = SgeJobParams(**json.load(json_file))
    container_working_directory = os.path.join(SHARED_VOLUME_PATH,
                                               params.job_name)
    return SgeJobParams(job_name=params.job_name,
                        shell_binary_path='/bin/bash',
                        threads=params.threads,
                        que=params.que,
                        golden_binary_path=params.golden_binary_path,
                        golden_reference_path=params.golden_reference_path,
                        input_path=os.path.join(container_working_directory,
                                                'input'),
                        working_dir_path=container_working_directory,
                        binary_path=os.path.join(container_working_directory,
                                                 'bin'),
                        output_path=os.path.join(container_working_directory,
                                                 'output'),
                        error_path=os.path.join(container_working_directory,
                                                'error'),
                        reference_path=os.path.join(
                            container_working_directory, 'ref'),
                        pipeline=params.pipeline)


def render_qsub_template(params: SgeJobParams) -> str:
    # FIXME find a better way to get the package absolute path
    package_path = qommunicator.__path__[0]  # type: ignore
    templates_folder = os.path.join(package_path, 'templates')
    file_loader = FileSystemLoader(searchpath=templates_folder)
    env = Environment(loader=file_loader)

    template = env.get_template('qsub_job.submit.j2')

    return template.render(params=params)


def create_qsub_job_file(filename: str, qsub_job: str) -> None:
    with open(filename, 'w') as qsub_file:
        qsub_file.writelines(qsub_job)

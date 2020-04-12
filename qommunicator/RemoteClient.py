import logging
from os import system
from typing import List

from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException

log = logging.getLogger(__name__)


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""
    def __init__(self,
                 host: str,
                 user: str,
                 ssh_key_path: str,
                 remote_path: str
    ):
        self.host = host
        self.user = user
        self.ssh_key_path = ssh_key_path
        self.remote_path = remote_path
        self.client = None
        self.scp = None
        # self.__upload_ssh_key()

    def __get_ssh_key(self) -> RSAKey:
        """Fetch locally stored SSH key."""
        try:
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_path)
            log.info(f'Found ssh key at self {self.ssh_key_path}')
        except SSHException as error:
            log.error(error)
        return self.ssh_key

    def __upload_ssh_key(self) -> None:
        """Upload locally stored ssh key"""
        try:
            system(f'ssh-copy-id -i {self.ssh_key_path} '
                   f'{self.user}@{self.host}>/dev/null 2>&1')
            system(f'ssh-copy-id -i {self.ssh_key_path}.pub '
                   f'{self.user}@{self.host}>/dev/null 2>&1')
            log.info(f'{self.ssh_key_path} uploaded to {self.host}')
        except FileNotFoundError as error:
            log.error(error)

    def __connect(self) -> SSHClient:
        """Open connection to remote host."""
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                key_filename=self.ssh_key_path,
                                look_for_keys=True,
                                timeout=5000)
            self.scp = SCPClient(self.client.get_transport())
        except AuthenticationException as error:
            log.info(f'Authentication failed.')
            log.error(error)
            raise error
        finally:
            return self.client

    def disconnect(self) -> None:
        """Close ssh connection."""
        self.client.close()
        self.scp.close()

    def execute_commands(self, commands: List[str]) -> None:
        """Execute multiple commands in succession"""
        if self.client is None:
            self.client = self.__connect()
        for command in commands:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                log.info(f'Input: {command} | Output: {line}')

    def bulk_upload(self, files: List[str]) -> None:
        """Upload multiple files to a remote directory"""
        if self.client is None:
            self.client = self.__connect()
        uploads = [self.____upload_file(file) for file in files]
        log.info(f'Uploaded {len(uploads)} files to {self.remote_path} on '
                 f'{self.host}')

    def ____upload_file(self, file: str) -> str:
        """Upload a single file to a remote directory"""
        try:
            self.scp.put(file,
                         recursice=True,
                         remote_path=self.remote_path)
        except SCPException as error:
            log.error(error)
            raise error
        finally:
            return file

    def download_file(self, file):
        if self.client is None:
            self.client = self.__connect()
        self.scp.get(file)


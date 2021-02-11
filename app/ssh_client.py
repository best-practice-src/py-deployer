from paramiko import SSHClient


class DeploySSHClient:
    def __init__(
            self,
            hostname: str,
            port: int,
            user: str,
            deploy_path: str,
            git_repository: str,
            password: str or None,
            identity_file: str or None
    ):
        self.hostname = hostname
        self.port = port
        self.user = user
        self.deploy_path = deploy_path
        self.git_repository = git_repository
        self.password = password
        self.identity_file = identity_file
        self.__ssh_client = SSHClient()
        self.__ssh_client.load_system_host_keys()

    def connect(self):
        self.__ssh_client.connect(
            self.hostname,
            self.port,
            self.user,
            self.password,
            self.identity_file
        )
        self.exec_command(f'mkdir -p {self.deploy_path}', False)

    def exec_command(self, command, cd_deploy_path=True) -> str:
        if cd_deploy_path:
            command = f'cd {self.deploy_path} && {command}'
        ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh_client.exec_command(command)
        ssh_stdin.channel.shutdown_write()

        stdout_msg = ssh_stdout.read().decode("utf8")
        stderr_msg = ssh_stderr.read().decode("utf8")
        exit_status = ssh_stdout.channel.recv_exit_status()

        ssh_stdin.close()
        ssh_stdout.close()
        ssh_stderr.close()

        if exit_status != 0:
            msg = stderr_msg.strip()
            if msg == '':
                msg = f'Command failed: {command} (Exit status: {exit_status})'
            raise IOError(msg)

        return stdout_msg

    def close(self):
        self.__ssh_client.close()

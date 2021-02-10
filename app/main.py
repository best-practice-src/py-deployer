from paramiko import SSHClient

from app.arguments import get_arguments
from app.config import get_stage_dict, get_config_dict


def main():
    args = get_arguments()
    stage_dict = get_stage_dict(args)
    config_dict = get_config_dict()
    stage = stage_dict.get('stage')

    print(f'Deploying {stage}...')

    ssh_client = DeploySSHClient(
        stage_dict.get('hostname'),
        stage_dict.get('port'),
        stage_dict.get('user'),
        stage_dict.get('deploy_path'),
        stage_dict.get('repository'),
        stage_dict.get('password'),
        stage_dict.get('identity_file')
    )

    ssh_client.connect()

    # Make releases folder (if does not exists)
    ssh_client.exec_command('mkdir -p releases')
    # Make shared folder (if does not exists)
    ssh_client.exec_command('mkdir -p shared')

    release_dirs = [int(d) for d in ssh_client.exec_command('ls releases/').split('\n') if d != '']
    release_dirs.sort()

    if len(release_dirs) == 0:
        current_release_dir = '1'
    else:
        current_release_dir = str(release_dirs[-1] + 1)

    # Clone branch inside new release directory
    branch = stage_dict.get("branch")
    repository = stage_dict.get("repository")

    print(f'Cloning {branch} inside release {current_release_dir}...')
    ssh_client.exec_command(f'git clone --single-branch --branch {branch} {repository} releases/{current_release_dir}')

    # Link shared files and directories
    print('Linking shared files and directories...')
    for shared_file in config_dict.get('shared'):
        # Touch shared file
        ssh_client.exec_command(f'touch shared/{shared_file}')
        # Link shared file into release folder
        ssh_client.exec_command(f'cd releases/{current_release_dir} && ln -s ../../shared/{shared_file}')

    print('Updated current link...')
    ssh_client.exec_command(f'rm -f current && ln -s releases/{current_release_dir} current')

    # Clean old release directories
    release_dirs = [int(d) for d in ssh_client.exec_command('ls releases/').split('\n') if d != '']
    release_dirs.sort()
    release_index = 0
    for release_dir in release_dirs[::-1]:
        release_index += 1
        if release_index > stage_dict.get('max_releases'):
            print(f'Deleting old release {release_dir}...')
            ssh_client.exec_command(f'rm -rf releases/{release_dir}')

    print('Done!')

    ssh_client.close()


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
        self.exec_command(f'mkdir -p {self.deploy_path}')

    def exec_command(self, command) -> str:
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
            print(stderr_msg)
            raise IOError(f'Return code: {exit_status}')

        return stdout_msg

    def close(self):
        self.__ssh_client.close()

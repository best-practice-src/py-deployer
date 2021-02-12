"""
*********************************************************************************
*                                                                               *
* main.py -- Main method.                                                       *
*                                                                               *
********************** IMPORTANT PY-DEPLOYER LICENSE TERMS **********************
*                                                                               *
* This file is part of py-deployer.                                             *
*                                                                               *
* py-deployer is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* py-deployer is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with py-deployer.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

import giturlparse
from paramiko.ssh_exception import AuthenticationException

from .arguments import get_arguments
from .config import Config
from .ssh_client import DeploySSHClient


def main():
    args = get_arguments()
    config = Config()
    stage_dict = config.get_stage_dict(args)
    config_dict = config.get_config_dict()
    stage = stage_dict.get('stage')
    repository_host = giturlparse.parse(stage_dict.get('repository')).host

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

    try:

        ssh_client.connect()

        print('Checking known_hosts...')
        repository_keys_output = ssh_client.exec_command(f'ssh-keyscan -H {repository_host}', False)
        repository_keys = [k for k in repository_keys_output.split('\n') if k != '']
        for repository_key in repository_keys:
            repository_key_no_hash = repository_key.split('= ')[1]
            try:
                current_keys_output = ssh_client.exec_command(
                    f"grep '{repository_key_no_hash}' ~/.ssh/known_hosts",
                    False
                )
                current_keys = [k for k in current_keys_output.split('\n') if k != '']
            except IOError:
                current_keys = []
            if len(current_keys) == 0:
                ssh_client.exec_command(f"echo '{repository_key}' >> ~/.ssh/known_hosts", False)
                print(f'Added {repository_host} key in ~/.ssh/known_hosts')

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
        ssh_client.exec_command(
            f'git clone --single-branch --branch {branch} {repository} releases/{current_release_dir}'
        )

        # Link shared files and directories
        print('Linking shared files and directories...')
        for shared_file in config_dict.get('shared'):
            # Touch shared file
            ssh_client.exec_command(f'touch shared/{shared_file}')
            # Link shared file into release folder
            ssh_client.exec_command(f'cd releases/{current_release_dir} && ln -s ../../shared/{shared_file}')

        print('Updating current link...')
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

    except IOError as e:
        print(str(e))
        return 10
    except AuthenticationException as e:
        print(str(e))
        print('Check your config.yaml')
        return 20

    print('Done!')
    ssh_client.close()
    return 0

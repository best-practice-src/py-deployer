"""
*********************************************************************************
*                                                                               *
* config.py -- Yaml configuration parsing.                                      *
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

import os
import sys
import git

from argparse import Namespace
from pathlib import Path

import yaml


class Config:
    __config_dict = None
    __cwd_path = Path(os.getcwd())
    __config_path = __cwd_path.joinpath('deploy').joinpath('config.yaml')
    __default_config_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.joinpath('deploy') \
        .joinpath('config_default.yaml')

    def __init__(self):
        with open(Config.__default_config_path) as default_config_file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.__default_config_dict = yaml.load(default_config_file, Loader=yaml.FullLoader).get('deploy')
        if not Config.__config_path.is_file():
            print("File ./deploy/config.yaml not found")
            sys.exit(3)
        with open(Config.__config_path) as config_file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.__config_dict = yaml.load(config_file, Loader=yaml.FullLoader).get('deploy')
        if self.__config_dict is None:
            print("'deploy' configuration not found. Check your config.yaml file")
            sys.exit(4)
        # Set default parameter
        # self.__default_config_dict | self.__config_dict
        self.__config_dict = Config.__merge_dicts(self.__default_config_dict, self.__config_dict)
        self.__check_config_dict('parameter', self.__config_dict, self.__default_config_dict)

    def get_stage_dict(self, args: Namespace) -> dict:
        servers_dict = self.__config_dict.get('servers')
        if servers_dict is None:
            print("'servers' configuration not found. Check your config.yaml file")
            sys.exit(4)

        stage_dict = None
        for stage in servers_dict.keys():
            server_dict = servers_dict.get(stage)
            if args.stage in (stage, server_dict.get('stage')):
                stage_dict = server_dict
                break

        if stage_dict is None:
            print("stage '" + args.stage + "' was not found.")
            sys.exit(5)

        default_stage_dict = self.__default_config_dict.get('servers').get('stage')

        if stage_dict.get('repository') is None:
            # Find Git repository
            try:
                stage_dict['repository'] = git.Git('.').remote('get-url', '--push', 'origin')
            except git.exc.GitCommandError:
                print('Git repository not found')
                sys.exit(6)

        self.__check_config_dict('Stage parameter', stage_dict, self.__default_config_dict.get('servers').get('stage'))

        # Merge real stage with default one
        return Config.__merge_dicts(default_stage_dict, stage_dict)

    def get_config_dict(self) -> dict:
        config_dict = {
            'shared': self.__config_dict.get('shared')
        }
        default_config_dict = {
            'shared': self.__default_config_dict.get('shared')
        }
        return Config.__merge_dicts(default_config_dict, config_dict)

    def __check_config_dict(self, parent_name: str, user_dict: dict, default_dict: dict):
        for default_key in default_dict.keys():
            # Check required parameters
            default_value = default_dict.get(default_key)
            user_value = user_dict.get(default_key)
            if default_value == '*' and (user_value == '*' or user_value is None):
                print(f"{parent_name} '{default_key}' is required! Check your config.yaml file")
                sys.exit(5)
            if type(user_value) is dict and type(default_value) is dict:
                self.__check_config_dict(default_key, user_value, default_value)

    @staticmethod
    def __merge_dicts(default_dict, user_dict) -> dict:
        return {**default_dict, **user_dict}

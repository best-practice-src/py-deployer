"""
*********************************************************************************
*                                                                               *
* arguments.py -- Argument parsing.                                             *
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

from . import settings
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
    """
    Return the input arguments
    :return: A Namespace
    """
    arg_parser = __get_argument_parser()
    args = arg_parser.parse_args()

    if args.version:
        print('v' + str(settings.VERSION))
        arg_parser.exit(0)

    if not args.stage:
        arg_parser.print_help()
        arg_parser.exit(0)

    return args


def __get_argument_parser() -> ArgumentParser:
    """
    Make a new ArgumentParser
    :return: An ArgumentParser
    """
    argument_parser = ArgumentParser(
        description=f"Py Deployer v{settings.VERSION}\n"
    )
    # --- Optional arguments ---#
    argument_parser.add_argument("-v", "--version", help="show program's version number and exit", action="store_true")
    argument_parser.add_argument("-s", "--stage", help="The stage to deploy", type=str)
    return argument_parser

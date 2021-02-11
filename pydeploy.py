#!/usr/bin/env python3

"""
*********************************************************************************
*                                                                               *
* pydeploy.py -- Main executable.                                               *
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

import sys

from app.main import main

if __name__ == "__main__":
    sys.exit(main())

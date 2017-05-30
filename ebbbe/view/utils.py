#!/usr/bin/env python
#
#
# 8-Bit Breadboard Emulator
#
# https://eartoearoak.com/ebbbe
#
# Copyright 2017 Al Brown
#
# An emulation of of Ben Eater's 8-bit breadboard computer (https://eater.net/8bit/)
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

from PySide.QtCore import Qt
import pkg_resources


def get_resource(resource):
    if not hasattr(sys, 'frozen'):
        return pkg_resources.resource_filename('ebbbe.view.res', resource)
    else:
        return os.path.join(sys._MEIPASS, 'res', resource)


def win_remove_context_help(window):
    flags = window.windowFlags()
    window.setWindowFlags(flags & (~Qt.WindowContextHelpButtonHint))

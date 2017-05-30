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

from PySide.QtGui import QDialog

from ebbbe.version import VERSION
from ebbbe.view import ui
from ebbbe.view.utils import win_remove_context_help


class DialogAbout(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        ui.load_ui(self, 'about.ui')
        win_remove_context_help(self)

        self._version.setText('v' + '.'.join([str(x) for x in VERSION]))

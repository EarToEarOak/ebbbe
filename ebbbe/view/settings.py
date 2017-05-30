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

from PySide.QtCore import QSettings


class Settings(object):
    def __init__(self):
        self.dirFile = '.'
        self.frequency = 30.

        self._settings = QSettings('Ear to Ear Oak', 'ebbbe')

        self.dirFile = self._settings.value('dirFile', self.dirFile)
        self.frequency = float(self._settings.value('frequency', self.frequency))

    def save(self):
        self._settings.setValue('dirFile', self.dirFile)
        self._settings.setValue('frequency', self.frequency)

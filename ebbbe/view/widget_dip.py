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

from PySide.QtCore import Signal
from PySide.QtGui import QWidget, QSizePolicy, QHBoxLayout, QSlider


class WidgetDip(QWidget):
    signalChanged = Signal(int)

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._dips = []

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)

    def __on_changed(self):
        value = self.get()
        self.signalChanged.emit(value)

    def set_dip_count(self, number):
        for i in range(number):
            dip = QSlider(self)
            dip.setMinimum(0)
            dip.setMaximum(1)
            dip.valueChanged.connect(self.__on_changed)
            self._layout.addWidget(dip)

            self._dips.append(dip)

    def enable(self, enabled):
        for dip in self._dips:
            dip.setEnabled(enabled)

    def get(self):
        value = 0
        for dip in self._dips:
            value <<= 1
            value |= dip.value()

        return value

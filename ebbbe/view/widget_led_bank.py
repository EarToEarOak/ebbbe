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

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

from ebbbe.view.constants import Colour
from ebbbe.view.widget_led import WidgetLed


class WidgetLedBank(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._leds = []

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)

    def set_led_count(self, number, colour=Colour.RED, names=None, tips=None, reverse=False):
        labels = []

        for i in range(number):
            layout = QVBoxLayout()
            led = WidgetLed(self, colour)
            label = QLabel(self)
            label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            layout.addWidget(led)
            layout.addWidget(label)
            self._layout.addLayout(layout)

            self._leds.append(led)
            labels.append(label)

        if not reverse:
            self._leds.reverse()
            labels.reverse()
            if names is not None:
                names.reverse()
            if tips is not None:
                tips.reverse()

        for i in range(number):
            if names is None:
                labels[i].setText(str(i))
            else:
                labels[i].setText(names[i])
            if tips is not None:
                self._leds[i].setToolTip(tips[i])
                labels[i].setToolTip(tips[i])

    def set(self, value):
        for led in self._leds:
            led.light(value & 0b1)
            value >>= 1

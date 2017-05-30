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

from PySide.QtCore import Slot
from PySide.QtGui import QWidget

from ebbbe.view.constants import Colour
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_led_bank import WidgetLedBank


class WidgetOut(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._twosComp = False
        self._value = 0

        self.customWidgets = {'WidgetLedBank': WidgetLedBank}

        load_ui(self, 'widget_out.ui')

        self._lcd.setStyleSheet('QLCDNumber {{background-color : black; color : {};}}'.format(Colour.BLUE))

        self.set(0)

    @Slot(bool)
    def on__buttonComp_clicked(self, checked):
        self._twosComp = checked
        self.__update()

    def __update(self):
        if not self._twosComp:
            value = self._value
        else:
            value = self._value if self._value >= 0 and self._value <= 127 else self._value - (1 << 8)

        self._lcd.display('{:0>3d}'.format(value))

    def set(self, value):
        self._value = value
        self.__update()
